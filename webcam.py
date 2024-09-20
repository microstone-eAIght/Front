import cv2
import numpy as np
import time

# 캠으로부터 데이터 가져오기
cap = cv2.VideoCapture(0)

# 캠으로부터 정보를 읽어들일 수 없는 경우 에러 메시지를 반환한다.
if cap.isOpened() == False:
    print("Unable to read camera")

# 캠으로부터 정보를 읽어들일 수 있으면
else:

    # 프레임의 정보 가져와 변수에 저장한다.
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # 타이머 시작
    start_time = time.time()
    out = None  # out을 초기화 (아직 정의되지 않았음을 명확히 하기 위해 None 사용)

    # 동영상을 20초마다 저장한다.
    while True:
        ret, frame = cap.read()
        if ret == True:

            # out이 None일 경우, 즉 첫 번째 프레임일 경우 파일을 연다.
            if out is None:
                current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
                out = cv2.VideoWriter(f'C:\\Users\\canpo\\Desktop\\dd\\output_{current_time}.avi',
                                      cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                      10,
                                      (frame_width, frame_height))

            # 20초가 경과했을 때 새로운 파일로 저장 시작
            if time.time() - start_time >= 20:
                # 기존 파일 저장 종료
                out.release()

                # 새로운 비디오 파일 열기
                current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
                out = cv2.VideoWriter(f'C:\\Users\\canpo\\Desktop\\dd\\output_{current_time}.avi',
                                      cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                      10,
                                      (frame_width, frame_height))
                
                # 타이머 리셋
                start_time = time.time()

            # 동영상 파일로 프레임 기록
            out.write(frame)

            # 화면에 프레임 출력
            cv2.imshow('frame', frame)

            # esc를 입력하면, 이미지를 받아오길 멈추게 한다.
            if cv2.waitKey(1) & 0xFF == 27:
                break
        else:
            break

    # 비디오 캡쳐와 파일 작성 종료
    cap.release()
    
    # 마지막 out 객체가 열려 있으면 종료
    if out is not None:
        out.release()

    # 화면에 띄운 창 닫기
    cv2.destroyAllWindows()
