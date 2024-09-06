import os
import torch
import cv2
import numpy as np
import csv
from ultralytics import YOLO
from reba import RebaScore
from owas import OwasScore

model = YOLO("yolov8m-pose.pt")

seconds = 1  # 동영상을 읽을 시간을 초 단위로 설정

# video_path = 'running.mp4'
# video_path = 'tumbling.mp4'
# video_path = 'yoga.mp4'
# video_path = 'walking2.mp4'
video_path = 'walking.mp4'  # video path

output_dir = 'results'  # 결과 저장 폴더

high_risk_dir = 'high_risk_images'  # High Risk 이미지 저장 폴더
csv_file_path = 'high_risk_info.csv'  # High Risk 정보 저장 CSV 파일

# 디렉토리 생성
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(high_risk_dir):
    os.makedirs(high_risk_dir)

# CSV 파일 초기화
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Frame', 'REBA Score C', 'OWAS Score', 'REBA Caption'])

def predict(frame, iou=0.7, conf=0.25):
    results = model(
        source=frame,
        device="0" if torch.cuda.is_available() else "cpu",
        iou=iou,  # 바운딩 박스 필터링 신뢰도 기준
        conf=conf,  # 모델이 탐지한 객체에 대한 최소 신뢰도 기준
        verbose=False,  # 추가 정보 출력 여부
    )
    result = results[0]  # 첫 번째 프레임의 이미지 (현재 1개씩의 프레임만 전달됨)
    return result

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

def extract_pose_from_yolo(result):
    keypoints = result.keypoints.data.cpu().numpy()  # 키포인트를 NumPy 배열로 변환
    kps = keypoints[0]  # 첫 번째 객체 (여기서는 사람)만 사용한다고 가정

    print(f"키포인트 개수: {len(kps)}")
    # print("키포인트: ", kps)

    if len(kps) < 17:
        raise ValueError("키포인트의 수가 예상보다 적습니다. 키포인트 수: {}".format(len(kps)))

    Lhip = kps[11][:2]  # Left Hip (x, y)
    Rhip = kps[12][:2]  # Right Hip (x, y)
    root_joint = (Lhip + Rhip) / 2
    
    selected_joints = [
        kps[5][:2],  # Left Shoulder
        kps[6][:2],  # Right Shoulder
        kps[7][:2],  # Left Elbow
        kps[8][:2],  # Right Elbow
        kps[9][:2],  # Left Wrist
        kps[10][:2],  # Right Wrist
        Lhip,  # Left Hip
        Rhip,  # Right Hip
        kps[13][:2],  # Left Knee
        kps[14][:2],  # Right Knee
        kps[15][:2],  # Left Ankle
        kps[16][:2],  # Right Ankle
        kps[0][:2],  # Nose
    ]
    
    transformed_joints = [joint - root_joint for joint in selected_joints]
    pose_3d = np.array([[x, y, 0] for x, y in transformed_joints])
    pose_with_root = np.vstack(([0, 0, 0], pose_3d))
    
    return pose_with_root

capture = cv2.VideoCapture(video_path)
if capture.get(cv2.CAP_PROP_POS_FRAMES) == capture.get(cv2.CAP_PROP_FRAME_COUNT):
    capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
fps = capture.get(cv2.CAP_PROP_FPS)  # 초당 프레임 수 얻기
total_frames = int(fps * seconds)  # seconds 시간 동안의 프레임 수
print('total 프레임:', total_frames)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

frame_count = 0
while frame_count < total_frames:
    ok, frame = capture.read()
    if not ok:
        print("프레임 읽기에 실패했습니다. 종료.")
        break
    result = predict(frame)  # 바운딩 박스와 키포인트 분석

    # 포즈 데이터를 입력 포즈 형식으로 변환
    pose = extract_pose_from_yolo(result)
    
    # REBA 분석
    rebaScore = RebaScore()
    body_params = rebaScore.get_body_angles_from_pose_right(pose)
    arms_params = rebaScore.get_arms_angles_from_pose_right(pose)
    
    rebaScore.set_body(body_params)
    score_a, partial_a = rebaScore.compute_score_a()
    
    rebaScore.set_arms(arms_params)
    score_b, partial_b = rebaScore.compute_score_b()
    
    score_c, caption = rebaScore.compute_score_c(score_a, score_b)
    
    print("REBA Score A: ", score_a, "Partial: ", partial_a)
    print("REBA Score B: ", score_b, "Partial: ", partial_b)
    print("REBA Score C: ", score_c, caption)

    # OWAS 분석
    owasScore = OwasScore()
    body_params_owas = owasScore.get_param_from_pose(pose, verbose=False)  # 'ppose'를 'pose'로 수정
    owasScore.set_body_params(body_params_owas)
    owas_score, partial_score = owasScore.compute_score()

    print("OWAS Score:", owas_score)
    print("Trunk, Arms, Legs, Load :", partial_score)

    # 키포인트 그리기 및 결과 저장
    results = draw_keypoints(result, frame)  # 분석된 내용으로 키포인트 연결

    # Very High Risk 필터링 및 저장
    if "Very High Risk" in caption:
        # 이미지 저장
        high_risk_image_path = os.path.join(high_risk_dir, f'high_risk_frame_{frame_count:04d}.jpg')
        cv2.imwrite(high_risk_image_path, frame)
        
        # 정보 저장
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([frame_count, score_c, owas_score, caption])

    output_path = os.path.join(output_dir, f'frame_{frame_count:04d}.jpg')
    cv2.imwrite(output_path, results)
    print("Saved to:", output_path)

    frame_count += 1
    key = cv2.waitKey(10)
    if key == ord('q'):
        print("사용자가 종료를 요청했습니다.")
        break

capture.release()
cv2.destroyAllWindows()
