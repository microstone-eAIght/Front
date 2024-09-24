from flask import Blueprint, render_template, request, redirect, session, flash
from models import Employee, db, Member
from forms import LoginForm, UserCreateForm, EmployeeCreateForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, get_flashed_messages
from lock import login_required

index_bp= Blueprint('index',__name__,)



@index_bp.route('/index')
@login_required
def index_view():
    if request.method == 'GET':
        # 사용자 이름 가져오기
        member = Member.query.filter_by(member_id=session['userid']).first()
        if member:
            member_name = member.member_name
        else:
            member_name = '이름 없음'

        return render_template('index.html', member_name=member_name)
    # 로그인이 되어 있는지 확인
    print("Session contents: ", session)

    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html')  # index.html 페이지로 이동
    else:
        return redirect('/')  # 로그인되지 않은 경우 로그인 페이지로 리다이렉트