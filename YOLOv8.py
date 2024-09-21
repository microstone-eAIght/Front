import os
import torch
import cv2
import numpy as np
import csv
from ultralytics import YOLO
from efficientnet_pytorch import EfficientNet  # EfficientNet 불러오기
from reba import RebaScore
from owas import OwasScore
from datetime import datetime, timedelta
import requests

# YOLOv8 모델 불러오기
model = YOLO("yolov8m-pose.pt")

# EfficientNet 모델 불러오기 (여기서는 b0 사용, 다른 버전도 선택 가능)
efficient_net = EfficientNet.from_pretrained('efficientnet-b7')

# seconds = 1  # 동영상에서 읽을 시간 설정 (초 단위)

# recorded_video_2024-09-09T09-48-38-912Z
# recorded_video_2024-09-09T09-48-38-random
# + 3시간을 추가

# 동영상 파일이 있는 디렉터리
directory = 'C:/video/'
# 동영상 파일 안에 있는 동영상의 제목은 무조건 recorded_video_%Y-%m-%dT%H-%M-%S.mp4 이 형식의 이름이어야 한다.
# recorded_video_년-월-일T시간-분-초.mp4
# 예를 들어 recorded_video_2024-09-09T09-48-38 이런 형식

# 결과 저장 폴더와 기타 디렉터리 설정
output_dir = 'C:/video/results'
high_risk_dir = 'C:/video/high_risk_images'
csv_file_path = 'C:/video/high_risk_info.csv'

# 디렉토리가 없을 경우 생성
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(high_risk_dir):
    os.makedirs(high_risk_dir)

# CSV 파일 초기화
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['프레임', 'REBA 점수 C', 'OWAS 점수', 'REBA 설명'])

# 동영상 파일 목록을 시간 순서대로 정렬하여 반환하는 함수
def get_sorted_video_files(directory):
    # 디렉터리 안의 파일 목록 가져오기
    files = [f for f in os.listdir(directory) if f.endswith('.mp4') or f.endswith('.webm') or f.endswith('.avi')]

    # 파일명에 포함된 시간을 파싱하여 정렬
    sorted_files = sorted(
        files,
        key=lambda x: datetime.strptime(x, 'output_%Y-%m-%d_%H-%M-%S.mp4') if x.endswith('.mp4')
        else datetime.strptime(x, 'output_%Y-%m-%d_%H-%M-%S.webm') if x.endswith('.webm')
        else datetime.strptime(x, 'output_%Y-%m-%d_%H-%M-%S.avi')
    )



    # 정렬된 파일 경로 반환
    return [os.path.join(directory, f) for f in sorted_files]

def predict(frame, iou=0.7, conf=0.25):
    results = model(
        source=frame,
        device="0" if torch.cuda.is_available() else "cpu",
        iou=iou,
        conf=conf,
        verbose=False,
    )
    result = results[0]
    return result

def refine_with_efficientnet(keypoints, frame):
    """ EfficientNet을 이미지 특징 추출기로 사용 """
    # EfficientNet에 입력할 프레임 크기를 224x224로 조정
    resized_frame = cv2.resize(frame, (224, 224))
    
    # 이미지를 EfficientNet 입력 형식에 맞게 변환
    input_tensor = torch.tensor(resized_frame).permute(2, 0, 1).unsqueeze(0).float() / 255.0  # 정규화
    input_tensor = input_tensor.to('cuda' if torch.cuda.is_available() else 'cpu')

    # EfficientNet을 통해 이미지 특징 추출
    with torch.no_grad():
        efficientnet_output = efficient_net.extract_features(input_tensor)
    
    # 특징을 기반으로 YOLOv8의 키포인트를 보정하는 로직을 추가 (사용자의 필요에 따라 조정)
    # 여기서는 YOLOv8의 결과를 그대로 사용
    return keypoints  # 현재는 키포인트를 보정하지 않고 그대로 반환

def draw_keypoints(result, frame):
# 신체 부위를 따라 키 포인트를 연결하는 리스트
  connections = [
      ([4, 2, 0, 1, 3], (0, 255, 0)), # 얼굴 부위. 초록
      ([10, 8, 6, 5, 7, 9], (255, 0, 0)), # 두 팔. 파랑
      ([6, 12, 11, 5], (255, 0, 255)), # 몸통. 보라
      ([12, 14, 16], (0, 165, 255)), # 오른 다리. 주홍
      ([11, 13, 15], (0, 165, 255)) # 왼 다리. 주홍
  ]

  for kps in result.keypoints: # predict()가 분석한 키 포인트의 원소를 순회
      kps = kps.data.squeeze() # 크기가 1인 불필요한 차원 제거
      nkps = kps.cpu().numpy() # 넘파이 배열로 변환

      for group, color in connections:
        for i in range(len(group) - 1):
          idx1, idx2 = group[i], group[i + 1] # 키 포인트와 이어야 하는 인접 키 포인트
          x1, y1, score1 = nkps[idx1] # x좌표, y좌표, 신뢰도 추출
          x2, y2, score2 = nkps[idx2] # x좌표, y좌표, 신뢰도 추출

          if score1 > 0.5 and score2 > 0.5: # 두 키 포인트의 신뢰도가 0.5보다 큰 경우에만
            point1 = (int(x1), int(y1)) # 키 포인트
            point2 = (int(x2), int(y2)) # 인접한 키 포인트

            cv2.circle(frame, point1, 3, (0, 0, 255), cv2.FILLED) # 각 키 포인트를 빨간색 원으로 그림
            cv2.putText(frame, str(idx1), point1, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)

            cv2.circle(frame, point2, 3, (0, 0, 255), cv2.FILLED) # 인접 키 포인트
            cv2.putText(frame, str(idx2), point2, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)

            cv2.line(frame, point1, point2, color, 2) # 두 키 포인트를 선으로 연결

  return frame # 키 포인트와 연결된 선이 그려진 frame 반환

def extract_pose_from_yolo(result, frame):
    keypoints = result.keypoints.data.cpu().numpy()
    
    if keypoints.shape[0] < 1:
        print("키포인트가 감지되지 않았습니다. 프레임을 건너뜁니다.")
        return None
    
    kps = keypoints[0]

    # EfficientNet으로 키포인트 개선
    refined_keypoints = refine_with_efficientnet(kps, frame)

    if len(refined_keypoints) < 17:
        print("감지된 키포인트가 충분하지 않습니다. 프레임을 건너뜁니다.")
        return None

    Lhip = refined_keypoints[11][:2]
    Rhip = refined_keypoints[12][:2]
    root_joint = (Lhip + Rhip) / 2

    selected_joints = [
        refined_keypoints[5][:2],  # 왼쪽 어깨
        refined_keypoints[6][:2],  # 오른쪽 어깨
        refined_keypoints[7][:2],  # 왼쪽 팔꿈치
        refined_keypoints[8][:2],  # 오른쪽 팔꿈치
        refined_keypoints[9][:2],  # 왼쪽 손목
        refined_keypoints[10][:2],  # 오른쪽 손목
        Lhip,  # 왼쪽 엉덩이
        Rhip,  # 오른쪽 엉덩이
        refined_keypoints[13][:2],  # 왼쪽 무릎
        refined_keypoints[14][:2],  # 오른쪽 무릎
        refined_keypoints[15][:2],  # 왼쪽 발목
        refined_keypoints[16][:2],  # 오른쪽 발목
        refined_keypoints[0][:2],  # 코
    ]

    transformed_joints = [joint - root_joint for joint in selected_joints]
    pose_3d = np.array([[x, y, 0] for x, y in transformed_joints])
    pose_with_root = np.vstack(([0, 0, 0], pose_3d))

    return pose_with_root

# 추출할 총 프레임 수 설정
total_frames_to_extract = 25  # 10초 동안 25개 프레임을 추출

# 동영상을 하나씩 불러오고 AI 처리 후 반복하는 함수
def process_videos(directory):
    sorted_videos = get_sorted_video_files(directory)
    
    for video_path in sorted_videos:
        print(f"현재 동영상 경로: {video_path}")

        # 동영상 파일명에서 시간을 추출하여 시작 시간으로 설정
        video_filename = os.path.basename(video_path)

        # 파일 확장자를 고려하여 .mp4나 .webm을 제거
        if video_filename.endswith('.mp4'):
            video_start_time_str = video_filename.split('_')[1] + "_" + video_filename.split('_')[2].replace('.mp4', '')
        elif video_filename.endswith('.webm'):
            video_start_time_str = video_filename.split('_')[1] + "_" + video_filename.split('_')[2].replace('.webm', '')
        elif video_filename.endswith('.avi'):
            video_start_time_str = video_filename.split('_')[1] + "_" + video_filename.split('_')[2].replace('.avi', '')

        video_start_time = datetime.strptime(video_start_time_str, '%Y-%m-%d_%H-%M-%S')

        capture = cv2.VideoCapture(video_path)
        fps = capture.get(cv2.CAP_PROP_FPS)  # 동영상의 FPS 값 가져오기
        total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))  # 동영상의 전체 프레임 수 가져오기

        # 25개의 프레임을 고르게 추출하기 위해 간격 계산
        frame_interval = max(1, total_frames // total_frames_to_extract)
        frame_count = 0
        extracted_frame_count = 0

        output_frame_count = 0

        while frame_count < total_frames and extracted_frame_count < total_frames_to_extract:
            ok, frame = capture.read()
            if not ok:
                print("프레임 읽기에 실패했습니다.")
                break

            # 여기에서 프레임 추출 조건을 만족할 때만 처리
            if frame_count % frame_interval == 0:
                result = predict(frame)
                pose = extract_pose_from_yolo(result, frame)

                 # 키포인트가 충분하지 않으면 다음 프레임으로 넘어감
                if pose is None:
                    frame_count += 1
                    continue

                # REBA 및 OWAS 계산 및 로그 출력
                rebaScore = RebaScore()

                # 여기서 pose가 None이면 진행을 멈추고 다음 프레임으로 넘어가야 함
                if pose is None:
                    print(f"프레임 {frame_count}: pose 값이 없습니다. 건너뜁니다.")
                    frame_count += 1
                    continue
                
                # 프레임 시간 계산
                frame_time_offset = frame_count / fps
                frame_time = video_start_time + timedelta(seconds=frame_time_offset)
                frame_time_str = frame_time.strftime('%Y-%m-%d_%H-%M-%S')
                frame_number_str = f"{frame_count:04d}"  # 4자리로 프레임 번호 표시
                frame_title = f'output_{frame_time_str}_{frame_number_str}.jpg'
                
                body_params = rebaScore.get_body_angles_from_pose_right(pose)
                arms_params = rebaScore.get_arms_angles_from_pose_right(pose)
                
                rebaScore.set_body(body_params)
                score_a, partial_a = rebaScore.compute_score_a()
                
                rebaScore.set_arms(arms_params)
                score_b, partial_b = rebaScore.compute_score_b()
                
                score_c, caption = rebaScore.compute_score_c(score_a, score_b)

                # 날짜를 추출하여 디렉토리 생성
                date_str = frame_time.strftime('%Y-%m-%d')
                date_dir = os.path.join(output_dir, date_str)
                if not os.path.exists(date_dir):
                    os.makedirs(date_dir)  # 날짜별 디렉토리 생성

                # 프레임 번호를 0, 1, 2, 3 순서대로 부여
                frame_number_str = f"{output_frame_count:04d}"  # 출력 프레임 번호를 사용
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

                ### 벡엔드야 여기를 봐~~
                # 점수를 전송하기 위한 POST 요청
                payload = {
                    'reba_score_a': int(score_a),                    # reba a 점수
                    'partial_a': [int(x) for x in partial_a],        # reba a 부분 점수 [목, 몸통, 다리]
                    'reba_score_b': int(score_b),                    # reba b 점수
                    'partial_b': [int(x) for x in partial_b],        # reba b 부분 점수 [어깨에서 팔꿈치까지, 팔꿈치에서 손목까지, 손목]
                    'reba_score_c': int(score_c),                    # reba 최종 점수
                    'caption': caption,                              # risk 단계
                    'owas_score': int(owas_score),                   # owas 점수
                    'partial_score': [int(x) for x in partial_score] # owas에서 나온 [몸통, 팔, 다리, 하중]
                }

                # response = requests.post("http://서버주소/api/scores", json=payload) # 시험 할 때는 여기 주석 풀고 주소 넣어서 해.
                ### 여기까지 포스트 넣어 봤어.

                results = draw_keypoints(result, frame)
                
                # 프레임이 동영상 시작 시간 이후 몇 초인지 계산
                frame_time_offset = frame_count / fps
                frame_time = video_start_time + timedelta(seconds=frame_time_offset)
                
                # 파일명에 시간을 반영하고 프레임 번호 추가하여 고유한 파일명 생성
                frame_time_str = frame_time.strftime('%Y-%m-%d_%H-%M-%S')
                frame_number_str = f"{frame_count:04d}"  # 4자리로 프레임 번호 표시

                # Very High Risk인 경우 프레임 저장 경로를 hi_risk_images/날짜로 변경
                high_risk_date_dir = os.path.join(high_risk_dir, date_str)
                if not os.path.exists(high_risk_date_dir):
                    os.makedirs(high_risk_date_dir)  # 날짜별 디렉토리 생성

                if "Very High Risk" in caption:
                    high_risk_image_path = os.path.join(high_risk_date_dir, f'high_risk_frame_{frame_time_str}_{output_frame_count}.jpg')
                    cv2.imwrite(high_risk_image_path, frame)
                    
                    with open(csv_file_path, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([frame_count, score_c, owas_score, caption])

                # 결과 이미지 저장
                output_path = os.path.join(date_dir, f'output_{frame_time_str}_{output_frame_count}.jpg')
                cv2.imwrite(output_path, results)

                # 추출된 프레임 수 증가
                extracted_frame_count += 1

                # 출력 프레임 카운터 증가
                output_frame_count += 1

            frame_count += 1
            key = cv2.waitKey(10)
            if key == ord('q'):
                print("사용자가 종료를 요청했습니다.")
                break

        capture.release()
        cv2.destroyAllWindows()

# 동영상 처리 함수 호출
process_videos(directory)
