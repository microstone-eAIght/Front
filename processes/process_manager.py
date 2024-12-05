import subprocess
import psutil
from flask import session
import time

# 실행 중인 프로세스를 저장하는 딕셔너리
processes = {}
scripts_running = False

def is_script_running(script_name):
    for proc in psutil.process_iter():
        if proc.name().lower() == 'python' and script_name in proc.cmdline():
            return True
    return False


# def start_scripts():
#     global scripts_running
#     if not scripts_running:
#         start_webcam_script()
#         start_yolo_script()
#         start_video_mover_script()
#         scripts_running = True  # 스크립트 실행 상태를 전역 변수로 관리

def start_scripts():
    global scripts_running
    if not scripts_running:
        start_webcam_script()  # webcam.py 먼저 실행
        time.sleep(3)  # 3초 대기
        start_video_mover_script()  # video_mover.py 실행
        time.sleep(2)  # 2초 대기
        start_yolo_script()  # YOLO모듈 최종.py 실행
        scripts_running = True  # 스크립트 실행 상태를 전역 변수로 관리

def start_webcam_script():
    if not is_script_running('webcam.py'):
        script_path = 'webcam.py'
        proc = subprocess.Popen(['python', script_path])
        processes['webcam'] = proc  # 프로세스를 저장

def start_yolo_script():
    if not is_script_running('YOLO모듈 최종.py'):
        script_path = 'AI/YOLO모듈 최종.py'
        proc = subprocess.Popen(['python', script_path])
        processes['yolo'] = proc  # 프로세스를 저장

def start_video_mover_script():
    if not is_script_running('video_mover.py'):
        script_path = 'AI/video_mover.py'
        proc = subprocess.Popen(['python', script_path])
        processes['video_mover'] = proc  # 프로세스를 저장

def stop_all_scripts():
    global processes  # 프로세스 목록을 전역 변수로 유지
    for script, proc in processes.items():
        if proc.poll() is None:  # 프로세스가 아직 실행 중인 경우
            proc.terminate()  # 프로세스 종료
            proc.wait()  # 종료될 때까지 대기
            print(f"{script} script has been terminated.")
    
    processes.clear()  # 모든 프로세스를 제거
    # 세션 상태 플래그를 False로 변경
    if 'scripts_running' in session:
        session['scripts_running'] = False
        session.modified = True




