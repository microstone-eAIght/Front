from flask import Blueprint, render_template, request, redirect, session, flash
from models import check_member_login
from flask import flash


login_bp= Blueprint('login',__name__)

@login_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  # 세션에서 사용자 ID 제거
    return '', 204  # No Content 응답 반환

@login_bp.route('/login', methods=['GET', 'POST'])
def login_view():
    userid = request.form.get(userid)
    password = request.form.get(password)

    if check_member_login(userid, password):
        session['user_id']=userid
        flash('로그인 성공!','success')
        return redirect('/index')
    else:
        flash('아이디 또는 비밀번호가 잘못 되었습니다.','error')
        redirect('/login')

    return render_template('login.html')