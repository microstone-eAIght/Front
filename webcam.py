import cv2
import time
import os

class WebcamVideoStream:
    def __init__(self, src=0, save_interval=20):
        # 비디오 저장 폴더 생성 (없으면)
        video_folder = 'C:/video'
        if not os.path.exists(video_folder):
            os.makedirs(video_folder)
            print(f"폴더 '{video_folder}' 생성됨")

        # 캠에서 데이터 가져오기
        self.stream = cv2.VideoCapture(src)
        self.stopped = False

        # 비디오 저장 관련 변수
        self.frame_width = int(self.stream.get(3))
        self.frame_height = int(self.stream.get(4))
        self.save_interval = save_interval  # 20초마다 저장
        self.start_time = time.time()  # 타이머 시작 시간
        self.out = None  # 비디오 파일 객체 초기화

    def start(self):
        # 실시간으로 프레임을 읽어오는 함수
        while not self.stopped:
            success, frame = self.stream.read()
            if success:
                # 스트리밍을 위해 프레임을 JPEG 형식으로 인코딩
                ret, jpeg = cv2.imencode('.jpg', frame)
                frame_bytes = jpeg.tobytes()

                # 20초마다 새로운 비디오 파일로 저장
                self.save_video(frame)  # 프레임을 비디오 파일로 저장
                
                # 스트리밍 데이터 반환
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            else:
                break

    def save_video(self, frame):
        # 20초마다 새로운 비디오 파일로 전환
        if time.time() - self.start_time >= self.save_interval:
            # 기존 비디오 파일 저장 종료
            if self.out is not None:
                self.out.release()

            # 새로운 비디오 파일 열기
            current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
            self.out = cv2.VideoWriter(f'C:/video/output_{current_time}.avi',
                                       cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                       25, (self.frame_width, self.frame_height))

            # 타이머 리셋 (새로운 비디오 파일을 시작할 때)
            self.start_time = time.time()

        # 프레임을 비디오 파일로 저장
        if self.out is not None:
            self.out.write(frame)

    def stop(self):
        # 비디오 스트림을 멈추고 자원을 해제하는 함수
        self.stopped = True
        self.stream.release()
        if self.out is not None:
            self.out.release()

# 웹캠에서 스트리밍하는 함수
def generate_frames():
    webcam_stream = WebcamVideoStream().start()
    return webcam_stream
