from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from models.login_model import check_member_login


login_bp= Blueprint('login',__name__)

@login_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('로그아웃 되었습니다.', 'info')
    return redirect(url_for('login.login_view'))

@login_bp.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        # 폼에서 입력된 사용자 ID와 비밀번호 가져오기
        userid = request.form.get('userid')
        password = request.form.get('password')

        # 로그인 검증
        if check_member_login(userid, password):
            session['user_id'] = userid
            session['logged_in'] = True
            flash('로그인 성공!', 'success')
            return redirect('/index')
        else:
            # 로그인 실패 시 오류 메시지와 함께 로그인 페이지로 리다이렉트
            flash('아이디 또는 비밀번호가 잘못되었습니다.', 'error')
            return redirect(url_for('login.login_view'))
        
    # GET 요청일 경우 로그인 페이지 렌더링
    return render_template('login.html')
