from flask import Blueprint, render_template, request, redirect, session, flash
from models import Employee, db, Member
from forms import LoginForm, UserCreateForm, EmployeeCreateForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, get_flashed_messages

from lock import login_required



bp= Blueprint('main',__name__,url_prefix='/')



@bp.route('/', methods=['GET', 'POST'])
def login():
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

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserCreateForm()

    if request.method == 'POST':
        # 입력 필드 유효성 검사
        if not form.userid or not form.password or not form.username or not form.userphone or not form.useremail or not form.useradd or not form.userposition:
            flash('모든 항목에 정보를 입력해주세요.', 'danger')
            return render_template('signup.html', form=form)

        # 회원 중복 체크
        if not Member.query.filter_by(member_id=form.userid).first():
            user = Member(
                member_id=form.userid,
                member_name=form.username,
                member_password=generate_password_hash(form.password),
                member_phone=form.userphone,
                member_email=form.useremail,
                member_address=form.useradd,
                member_position=form.userposition
            )

            db.session.add(user)
            db.session.commit()
            session.pop('_flashes', None)  # 이전 플래시 메시지 제거
            return redirect('/')

        else:
            flash('이미 존재하는 사용자입니다.', 'danger')

    return render_template('signup.html', form=form)


@bp.route('/employee', methods=['GET', 'POST'])
@login_required
def employee_view():
    if request.method == 'GET':
        employees = Employee.query.all()
        return render_template('employee.html', employees=employees)
    elif request.method == 'POST':
        emp_name = request.form.get('name')
        emp_add = request.form.get('region')
        emp_department = request.form.get('department')
        emp_position = request.form.get('position')
        emp_phone = request.form.get('phone')
        emp_email = request.form.get('email')

        new_employee = Employee(
            employee_name=emp_name, employee_address=emp_add,
            employee_department=emp_department, employee_position=emp_position,
            employee_phone=emp_phone, employee_email=emp_email
        )

        db.session.add(new_employee)
        db.session.commit()
        return redirect('/employee')


@bp.route('/index')
@login_required
def index_view():
    # 로그인이 되어 있는지 확인
    print("Session contents: ", session)

    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html')  # index.html 페이지로 이동
    else:
        return redirect('/')  # 로그인되지 않은 경우 로그인 페이지로 리다이렉트


@bp.route('/storage')
@login_required
def storage_view():
        return render_template('storage.html')