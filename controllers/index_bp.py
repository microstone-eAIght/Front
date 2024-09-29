from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash
from models import get_member_name
from flask import flash, get_flashed_messages
from lock import login_required

index_bp= Blueprint('main',__name__,)



@index_bp.route('/index')
@login_required
def index_view():
    if request.method == 'GET':
        # 세션 내용 출력 (디버깅 용도로 사용)
        print("Session contents: ", session)

        if 'user_id' in session and session['user_id']:
            # 로그인 되어 있으면 사용자 이름 가져오기
            member_name = get_member_name()

            # 사용자 이름이 있으면 해당 이름을 전달하여 페이지 렌더링
            return render_template('index.html', member_name=member_name)
        else:
            # 로그인되어 있지 않으면 로그인 페이지로 리다이렉트
            return redirect('/')