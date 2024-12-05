import cv2
import time
import os

class WebcamVideoStream:
    def __init__(self, src=0, save_interval=20):
        video_folder = 'C:/video/'
        if not os.path.exists(video_folder):
            os.makedirs(video_folder)
            print(f"폴더 '{video_folder}' 생성됨")

        self.stream = cv2.VideoCapture(src)
        self.stopped = False

        self.frame_width = int(self.stream.get(3))
        self.frame_height = int(self.stream.get(4))
        self.save_interval = save_interval  # 20초마다 저장
        self.start_time = time.time()  # 타이머 시작 시간
        self.out = None
        self.lock_file_path = None  # 잠금 파일 경로

    def start(self):
        while not self.stopped:
            success, frame = self.stream.read()
            if success:
                ret, jpeg = cv2.imencode('.jpg', frame)
                frame_bytes = jpeg.tobytes()

                # 20초마다 새로운 비디오 파일로 저장
                self.save_video(frame)

                # 스트리밍 데이터 반환
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            else:
                break

    def save_video(self, frame):
        # 20초마다 새로운 비디오 파일로 전환
        if time.time() - self.start_time >= self.save_interval:
            if self.out is not None:
                # 기존 비디오 파일 작업 완료 시 잠금 파일 해제
                self.release_lock()
                self.out.release()
                self.out = None

            # 새로운 비디오 파일 열기
            current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
            self.out = cv2.VideoWriter(f'C:/video/output_{current_time}.avi',
                                       cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                       25, (self.frame_width, self.frame_height))

            # 새 비디오 파일 작업 시 잠금 파일 생성
            self.create_lock(f'C:/video/output_{current_time}.avi')

            self.start_time = time.time()

        # 프레임을 비디오 파일로 저장
        if self.out is not None:
            self.out.write(frame)

    def create_lock(self, video_path):
        """비디오 파일에 대한 잠금 파일 생성"""
        self.lock_file_path = video_path + '.lock'
        with open(self.lock_file_path, 'w') as lock_file:
            lock_file.write('LOCKED')
        print(f"잠금 파일 생성: {self.lock_file_path}")

    def release_lock(self):
        """잠금 파일 삭제"""
        if self.lock_file_path and os.path.exists(self.lock_file_path):
            os.remove(self.lock_file_path)
            print(f"잠금 파일 해제: {self.lock_file_path}")
        self.lock_file_path = None

    def stop(self):
        self.stopped = True
        self.stream.release()
        if self.out is not None:
            self.release_lock()
            self.out.release()

def generate_frames():
    webcam_stream = WebcamVideoStream().start()
    return webcam_stream
