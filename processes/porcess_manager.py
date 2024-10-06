import subprocess
import psutil

# 실행 중인 프로세스를 저장하는 리스트
processes = []

def is_script_running(script_name):
    for proc in psutil.process_iter():
        if proc.name().lower() == 'python' and script_name in proc.cmdline():
            return True
    return False

def start_webcam_script():
    if not is_script_running('webcam.py'):
        script_path = 'webcam.py'
        subprocess.Popen(['python', script_path])

def start_yolo_script():
    if not is_script_running('YOLO모듈 최종.py'):
        script_path = 'AI/YOLO모듈 최종.py'
        subprocess.Popen(['python', script_path])

def start_video_mover_script():
    if not is_script_running('video_mover.py'):
        script_path = 'AI/video_mover.py'
        subprocess.Popen(['python', script_path])

def terminate_processes():
    for proc in processes:
        if proc.poll() is None:  # 프로세스가 아직 실행 중이라면
            proc.terminate()  # 프로세스 종료
            proc.wait()  # 종료될 때까지 대기