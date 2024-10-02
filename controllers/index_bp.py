from flask import Blueprint, render_template, request, redirect, session, flash
from models import Employee, db, Member
from forms import LoginForm, UserCreateForm, EmployeeCreateForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, get_flashed_messages
from lock import login_required

# index_bp= Blueprint('index',__name__,)



# @index_bp.route('/index')
# @login_required
# def index_view():
#     # 로그인이 되어 있는지 확인
#     print("Session contents: ", session)

#     if 'logged_in' in session and session['logged_in']:
#         return render_template('index.html')  # index.html 페이지로 이동
#     else:
#         return redirect('/')  # 로그인되지 않은 경우 로그인 페이지로 리다이렉트



from flask import Blueprint, render_template, redirect, session
import subprocess
import os

index_bp = Blueprint('index', __name__)

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
    if 'logged_in' in session and session['logged_in']:
        # 로그인 후 백그라운드 작업 시작
        start_webcam_script()  # 웹캠 스크립트 실행
        start_yolo_script()  # YOLO 스크립트 실행
        start_video_mover_script()  # video_mover 스크립트 실행
        return render_template('index.html')  # index.html 페이지로 이동
    else:
        return redirect('/')  # 로그인되지 않은 경우 로그인 페이지로 리다이렉트