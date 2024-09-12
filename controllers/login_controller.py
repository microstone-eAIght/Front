from flask import Blueprint, render_template, request, redirect, session
from models import Member, db

login_bp = Blueprint('login', __name__)

@login_bp.route('/', methods=['GET', 'POST'])
def login_view():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        userid = request.form.get('아이디')
        password = request.form.get('비밀번호')

        # 데이터베이스에서 사용자 조회 (ORM을 사용한 방식)
        user = Member.query.filter_by(member_id=userid, member_password=password).first()

        if user:
            session['logged_in'] = True
            session['userid'] = userid
            return redirect('/index')
        else:
            return "로그인 실패"
