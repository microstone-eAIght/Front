from flask import Blueprint, render_template, request, redirect, session, Response, flash
from models.index_model import get_member_name
from lock import login_required
from webcam import generate_frames
from processes.porcess_manager import start_webcam_script, start_yolo_script, start_video_mover_script, stop_all_scripts

index_bp= Blueprint('main',__name__,)

@index_bp.route('/logout')
def logout():
    stop_all_scripts()
    session.clear()
    flash('로그아웃 되었습니다.', 'info')
    return redirect('/')


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
        
@index_bp.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
