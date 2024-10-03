from flask import Blueprint, render_template, request, redirect, session, flash
from models.index_model import get_member_name
from lock import login_required
import subprocess
import os

index_bp= Blueprint('main',__name__,)

# 스크립트를 실행하는 함수 (webcam.py와 YOLOv8모듈 최종.py 실행)
def start_webcam_script():
    # webcam.py 스크립트를 백그라운드에서 실행
    script_path = 'webcam.py' # webcam.py 경로
    subprocess.Popen(['python', script_path])

def start_yolo_script():
    # YOLOv8모듈 최종.py 스크립트를 백그라운드에서 실행
    script_path = 'AI/YOLO모듈 최종.py' # YOLOv8모듈 최종.py 경로
    subprocess.Popen(['python', script_path])

def start_video_mover_script():
    # video_mover.py 스크립트를 백그라운드에서 실행
    script_path = 'AI/video_mover.py'
    subprocess.Popen(['python', script_path])

@index_bp.route('/index')
@login_required
def index_view():
    if request.method == 'GET':
        # 세션 내용 출력 (디버깅 용도로 사용)
        print("Session contents: ", session)

        if 'user_id' in session and session['user_id']:
            # 로그인 되어 있으면 사용자 이름 가져오기
            member_name = get_member_name()

            start_webcam_script()  # 웹캠 스크립트 실행
            start_yolo_script()  # YOLO 스크립트 실행
            start_video_mover_script()  # video_mover 스크립트 실행

            # 사용자 이름이 있으면 해당 이름을 전달하여 페이지 렌더링
            return render_template('index.html', member_name=member_name)
        else:
            # 로그인되어 있지 않으면 로그인 페이지로 리다이렉트
            return redirect('/')