from flask import Blueprint, render_template, request, redirect, session, flash
from models import Employee, db, Member
from forms import LoginForm, UserCreateForm, EmployeeCreateForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, get_flashed_messages

from lock import login_required



login_bp= Blueprint('main',__name__,url_prefix='/')



@login_bp.route('/', methods=['GET', 'POST'])
def login_view():
    form = LoginForm()

    if request.method == 'POST':
        user = Member.query.filter_by(member_id=form.userid).first()

        # 사용자 정보가 있는지 확인
        print(f"Form userid: {form.userid}")
        if not user:
            print("User not found.")
        else:
            print(f"User found: {user.member_id}")
            print(f"Input password: {form.password}")
            print(f"Stored hash: {user.member_password}")

        # 비밀번호 검증
        if user and check_password_hash(user.member_password, form.password):
            session['logged_in'] = True
            session['userid'] = user.member_id
            print("Login successful, session contents: ", session)
            session.pop('_flashes', None)
            return redirect('/index')

        flash('아이디 혹은 비밀번호를 확인해 주세요.', 'danger')

    return render_template('login.html', form=form)
