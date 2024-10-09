from flask import Blueprint, render_template, request, redirect, session, Response, flash
from models.index_model import get_member_name
from lock import login_required
from webcam import generate_frames
from processes.process_manager import start_scripts, stop_all_scripts

index_bp= Blueprint('main',__name__,)

@index_bp.route('/logout')
def logout():
    stop_all_scripts()
    session.clear()
    session['scripts_running'] = False
    session.modified = True  # 세션 변경 여부를 Flask에 알림
    flash('로그아웃 되었습니다.', 'info')
    print("Session contents: ", session)

    return redirect('/')


@index_bp.route('/index')
@login_required
def index_view():
    if request.method == 'GET':
        # 세션 내용 출력 (디버깅 용도로 사용)
        print("Session contents: ", session)

        if session.get('logged_in'):
            member_name = get_member_name()

            if 'scripts_running' not in session:
                    session['scripts_running'] = False  # 기본값은 False로 설정
                    session.modified = True

            if not session.get('scripts_running'):
                    start_scripts()
                    session['scripts_running'] = True  # 스크립트 실행 여부 플래그 설정
                    session.modified = True


            # 사용자 이름이 있으면 해당 이름을 전달하여 페이지 렌더링
            return render_template('index.html', member_name=member_name)
        else:
            # 로그인되어 있지 않으면 로그인 페이지로 리다이렉트
            return redirect('/')
        
@index_bp.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
