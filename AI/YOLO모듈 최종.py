import os
import time
import torch
import cv2
import numpy as np
import csv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ultralytics import YOLO
from efficientnet_pytorch import EfficientNet
from reba import RebaScore
from owas import OwasScore
from datetime import datetime, timedelta
import requests
from database_handler import save_to_database

class VideoProcessor(FileSystemEventHandler):
    def __init__(self):
        self.video_directory = 'C:/video_AI/'
        self.output_dir = 'C:/video_AI/results'
        self.high_risk_dir = 'C:/video_AI/high_risk_images'
        self.csv_file_path = 'C:/video_AI/high_risk_info.csv'
        self.total_frames_to_extract = 25

        # YOLOv8 모델과 EfficientNet 모델 로드
        self.model = YOLO("yolov8m-pose.pt")
        self.efficient_net = EfficientNet.from_pretrained('efficientnet-b7')

        # 디렉토리 준비
        self._prepare_directories()

        # CSV 파일 초기화
        with open(self.csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['프레임', 'REBA 점수 C', 'OWAS 점수', 'REBA 설명'])

    def _prepare_directories(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        if not os.path.exists(self.high_risk_dir):
            os.makedirs(self.high_risk_dir)

    def on_created(self, event):
        # 새 파일이 생성될 때 이 메서드가 호출됩니다.
        if event.src_path.endswith(('.mp4', '.webm', '.avi')):
            print(f"새 동영상 파일이 감지되었습니다: {event.src_path}")
            self.process_video(event.src_path)

    def get_sorted_video_files(self):
        files = [f for f in os.listdir(self.video_directory) if f.endswith('.mp4') or f.endswith('.webm') or f.endswith('.avi')]
        sorted_files = sorted(
            files,
            key=lambda x: datetime.strptime(x, 'output_%Y-%m-%d_%H-%M-%S.mp4') if x.endswith('.mp4')
            else datetime.strptime(x, 'output_%Y-%m-%d_%H-%M-%S.webm') if x.endswith('.webm')
            else datetime.strptime(x, 'output_%Y-%m-%d_%H-%M-%S.avi')
        )
        return [os.path.join(self.video_directory, f) for f in sorted_files]

    def refine_with_efficientnet(self, keypoints, frame):
        resized_frame = cv2.resize(frame, (224, 224))
        input_tensor = torch.tensor(resized_frame).permute(2, 0, 1).unsqueeze(0).float() / 255.0
        input_tensor = input_tensor.to('cuda' if torch.cuda.is_available() else 'cpu')

        with torch.no_grad():
            efficientnet_output = self.efficient_net.extract_features(input_tensor)

        return keypoints

    def process_video(self, video_path):
        print(f"동영상 처리 시작: {video_path}")
        video_filename = os.path.basename(video_path)

        # 파일 이름에서 시간 정보 추출
        if video_filename.endswith('.mp4'):
            video_start_time_str = video_filename.split('_')[1] + "_" + video_filename.split('_')[2].replace('.mp4', '')
        elif video_filename.endswith('.webm'):
            video_start_time_str = video_filename.split('_')[1] + "_" + video_filename.split('_')[2].replace('.webm', '')
        elif video_filename.endswith('.avi'):
            video_start_time_str = video_filename.split('_')[1] + "_" + video_filename.split('_')[2].replace('.avi', '')

        video_start_time = datetime.strptime(video_start_time_str, '%Y-%m-%d_%H-%M-%S')

        capture = cv2.VideoCapture(video_path)
        fps = capture.get(cv2.CAP_PROP_FPS)
        total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_interval = max(1, total_frames // self.total_frames_to_extract)
        frame_count = 0
        extracted_frame_count = 0
        output_frame_count = 0

        while frame_count < total_frames and extracted_frame_count < self.total_frames_to_extract:
            ok, frame = capture.read()
            if not ok:
                print("프레임 읽기에 실패했습니다.")
                break

            if frame_count % frame_interval == 0:
                result = self.predict(frame)
                pose = self.extract_pose_from_yolo(result, frame)

                if pose is None:
                    print(f"프레임 {frame_count}: pose 값이 없습니다. 건너뜁니다.")
                    frame_count += 1
                    continue

                rebaScore = RebaScore()
                body_params = rebaScore.get_body_angles_from_pose_right(pose)
                arms_params = rebaScore.get_arms_angles_from_pose_right(pose)

                rebaScore.set_body(body_params)
                score_a, partial_a = rebaScore.compute_score_a()
                rebaScore.set_arms(arms_params)
                score_b, partial_b = rebaScore.compute_score_b()
                score_c, caption = rebaScore.compute_score_c(score_a, score_b)

                date_str = video_start_time.strftime('%Y-%m-%d')
                date_dir = os.path.join(self.output_dir, date_str)
                if not os.path.exists(date_dir):
                    os.makedirs(date_dir)

                frame_time_offset = frame_count / fps
                frame_time = video_start_time + timedelta(seconds=frame_time_offset)
                frame_time_str = frame_time.strftime('%Y-%m-%d_%H-%M-%S')
                frame_number_str = f"{output_frame_count:04d}"
                frame_title = f'output_{frame_time_str}_{frame_number_str}.jpg'

                print(f"프레임 제목: {frame_title}")
                print("REBA 점수 A: ", score_a, "부분 점수: ", partial_a)
                print("REBA 점수 B: ", score_b, "부분 점수: ", partial_b)
                print("REBA 점수 C: ", score_c, caption)

                owasScore = OwasScore()
                body_params_owas = owasScore.get_param_from_pose(pose)
                owasScore.set_body_params(body_params_owas)
                owas_score, partial_score = owasScore.compute_score()

                # print(f"Trunk: {partial_score[0]}, Arms: {partial_score[1]}, Legs: {partial_score[2]}, Load: {partial_score[3]}")
                print("OWAS 점수:", owas_score)
                print("몸통, 팔, 다리, 하중:", partial_score)

                results = self.draw_keypoints(result, frame)

                # 프레임이 동영상 시작 시간 이후 몇 초인지 계산
                frame_time_offset = frame_count / fps
                frame_time = video_start_time + timedelta(seconds=frame_time_offset)
                
                # 파일명에 시간을 반영하고 프레임 번호 추가하여 고유한 파일명 생성
                frame_time_str = frame_time.strftime('%Y-%m-%d_%H-%M-%S')
                frame_number_str = f"{frame_count:04d}"  # 4자리로 프레임 번호 표시

                # Very High Risk인 경우 프레임 저장 경로를 hi_risk_images/날짜로 변경
                # high_risk_date_dir = os.path.join(self.high_risk_dir, date_str)
                # if not os.path.exists(high_risk_date_dir):
                #     os.makedirs(high_risk_date_dir)  # 날짜별 디렉토리 생성


                if "High Risk" in caption:
                        high_risk_image_path = os.path.join(self.high_risk_dir, frame_title) # f'output_{frame_time_str}_{output_frame_count}.jpg'
                        cv2.imwrite(high_risk_image_path, frame)

                        # 이미지 파일을 읽어서 바이너리 형태로 서버로 전송
                        with open(high_risk_image_path, 'rb') as img_file:
                            image_payload = {
                                'frame_title': frame_title,                 # 프레임 제목
                                'reba_score_a': int(score_a),                    # reba a 점수
                                'partial_a': [int(x) for x in partial_a],        # reba a 부분 점수 [목, 몸통, 다리]
                                'reba_score_b': int(score_b),                    # reba b 점수
                                'partial_b': [int(x) for x in partial_b],        # reba b 부분 점수 [어깨에서 팔꿈치까지, 팔꿈치에서 손목까지, 손목]
                                'reba_score_c': int(score_c),                    # reba 최종 점수
                                'caption': caption,                              # risk 단계
                                'owas_score': int(owas_score),                   # owas 점수
                                'partial_score': [int(x) for x in partial_score] # owas에서 나온 [몸통, 팔, 다리, 하중]
                            }
                            
                            files = {'image': img_file}

                            # 데이터베이스에 저장
                            save_to_database(image_payload)  # 새로 만든 함수 호출
                            
                            # POST 요청 전송 (이미지 포함)
                            # response = requests.post("http://서버주소/api/high_risk_images", data=image_payload, files=files)

                            # 응답 확인
                            # if response.status_code == 200:
                            #     print("Very High Risk 이미지가 성공적으로 전송되었습니다.")
                            # else:
                            #     print(f"이미지 전송에 실패했습니다. 상태 코드: {response.status_code}")
                        
                        with open(self.csv_file_path, mode='a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([frame_count, score_c, owas_score, caption])

                output_path = os.path.join(date_dir, f'output_{frame_time_str}_{output_frame_count}.jpg')
                results_frame = self.draw_keypoints(result, frame)
                cv2.imwrite(output_path, results_frame)

                extracted_frame_count += 1
                output_frame_count += 1

            frame_count += 1

        capture.release()
        cv2.destroyAllWindows()

    def predict(self, frame, iou=0.7, conf=0.25):
        results = self.model(
            source=frame,
            device="0" if torch.cuda.is_available() else "cpu",
            iou=iou,
            conf=conf,
            verbose=False,
        )
        return results[0]

    def extract_pose_from_yolo(self, result, frame):
        keypoints = result.keypoints.data.cpu().numpy()

        if keypoints.shape[0] < 1:
            print("키포인트가 감지되지 않았습니다. 프레임을 건너뜁니다.")
            return None

        kps = keypoints[0]
        refined_keypoints = self.refine_with_efficientnet(kps, frame)

        if len(refined_keypoints) < 17:
            print("감지된 키포인트가 충분하지 않습니다. 프레임을 건너뜁니다.")
            return None

        Lhip = refined_keypoints[11][:2]
        Rhip = refined_keypoints[12][:2]
        root_joint = (Lhip + Rhip) / 2

        selected_joints = [
            refined_keypoints[5][:2], refined_keypoints[6][:2],
            refined_keypoints[7][:2], refined_keypoints[8][:2],
            refined_keypoints[9][:2], refined_keypoints[10][:2],
            Lhip, Rhip,
            refined_keypoints[13][:2], refined_keypoints[14][:2],
            refined_keypoints[15][:2], refined_keypoints[16][:2],
            refined_keypoints[0][:2],
        ]

        transformed_joints = [joint - root_joint for joint in selected_joints]
        pose_3d = np.array([[x, y, 0] for x, y in transformed_joints])
        return np.vstack(([0, 0, 0], pose_3d))

    def draw_keypoints(self, result, frame):
        connections = [
            ([4, 2, 0, 1, 3], (0, 255, 0)),
            ([10, 8, 6, 5, 7, 9], (255, 0, 0)),
            ([6, 12, 11, 5], (255, 0, 255)),
            ([12, 14, 16], (0, 165, 255)),
            ([11, 13, 15], (0, 165, 255))
        ]

        for kps in result.keypoints:
            kps = kps.data.squeeze()
            nkps = kps.cpu().numpy()

            for group, color in connections:
                for i in range(len(group) - 1):
                    idx1, idx2 = group[i], group[i + 1]
                    x1, y1, score1 = nkps[idx1]
                    x2, y2, score2 = nkps[idx2]

                    if score1 > 0.5 and score2 > 0.5:
                        point1 = (int(x1), int(y1))
                        point2 = (int(x2), int(y2))

                        cv2.circle(frame, point1, 3, (0, 0, 255), cv2.FILLED)
                        cv2.putText(frame, str(idx1), point1, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
                        cv2.circle(frame, point2, 3, (0, 0, 255), cv2.FILLED)
                        cv2.putText(frame, str(idx2), point2, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
                        cv2.line(frame, point1, point2, color, 2)

        return frame

    def process_videos(self):
        # Watchdog을 사용해 파일 생성 감시 및 처리
        event_handler = self
        observer = Observer()
        observer.schedule(event_handler, path=self.video_directory, recursive=False)

        print("파일 감시 시작")
        observer.start()

        try:
            while True:
                time.sleep(1)  # 무한 루프를 통해 계속 감시
        except KeyboardInterrupt:
            print("감시 중지 요청을 받았습니다.")
        finally:
            observer.stop()
            observer.join()

# 사용 예시
if __name__ == "__main__":
    video_processor = VideoProcessor()
    video_processor.process_videos()
