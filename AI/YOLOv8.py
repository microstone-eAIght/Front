import os
import torch
import cv2
import numpy as np
import csv
from ultralytics import YOLO
from efficientnet_pytorch import EfficientNet  # EfficientNet 불러오기
from reba import RebaScore
from owas import OwasScore

# YOLOv8 모델 불러오기
model = YOLO("yolov8m-pose.pt")

# EfficientNet 모델 불러오기 (여기서는 b0 사용, 다른 버전도 선택 가능)
efficient_net = EfficientNet.from_pretrained('efficientnet-b7')

seconds = 1  # 동영상에서 읽을 시간 설정 (초 단위)

# video_path = 'running.mp4'
# video_path = 'tumbling.mp4'
# video_path = 'yoga.mp4'
video_path = 'walking2.mp4'
# video_path = 'walking.mp4'  # video path

output_dir = 'results'  # 결과 저장 폴더

high_risk_dir = 'high_risk_images'  # High Risk 이미지 저장 폴더
csv_file_path = 'high_risk_info.csv'  # High Risk 정보 저장 CSV 파일

# 디렉토리가 없을 경우 생성
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(high_risk_dir):
    os.makedirs(high_risk_dir)

# CSV 파일 초기화
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['프레임', 'REBA 점수 C', 'OWAS 점수', 'REBA 설명'])

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

def extract_pose_from_yolo(result):
    keypoints = result.keypoints.data.cpu().numpy()
    kps = keypoints[0]

    # EfficientNet으로 키포인트 개선
    refined_keypoints = refine_with_efficientnet(kps, frame)

    if len(refined_keypoints) < 17:
        raise ValueError("감지된 키포인트가 충분하지 않습니다.")

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

capture = cv2.VideoCapture(video_path)
fps = capture.get(cv2.CAP_PROP_FPS)
total_frames = int(fps * seconds)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

frame_count = 0
while frame_count < total_frames:
    ok, frame = capture.read()
    if not ok:
        print("프레임 읽기에 실패했습니다.")
        break
    result = predict(frame)

    # YOLOv8 결과를 EfficientNet으로 개선
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
    
    print("REBA 점수 A: ", score_a, "부분 점수: ", partial_a)
    print("REBA 점수 B: ", score_b, "부분 점수: ", partial_b)
    print("REBA 점수 C: ", score_c, caption)

    # OWAS 분석
    owasScore = OwasScore()
    body_params_owas = owasScore.get_param_from_pose(pose)
    owasScore.set_body_params(body_params_owas)
    owas_score, partial_score = owasScore.compute_score()

    print("OWAS 점수:", owas_score)
    print("몸통, 팔, 다리, 하중:", partial_score)

    # 키포인트 그리기 및 결과 저장
    results = draw_keypoints(result, frame)
    
    if "Very High Risk" in caption:
        high_risk_image_path = os.path.join(high_risk_dir, f'high_risk_frame_{frame_count:04d}.jpg')
        cv2.imwrite(high_risk_image_path, frame)
        
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([frame_count, score_c, owas_score, caption])

    output_path = os.path.join(output_dir, f'frame_{frame_count:04d}.jpg')
    cv2.imwrite(output_path, results)

    frame_count += 1
    key = cv2.waitKey(10)
    if key == ord('q'):
        print("사용자가 종료를 요청했습니다.")
        break

capture.release()
cv2.destroyAllWindows()
