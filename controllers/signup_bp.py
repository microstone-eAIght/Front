from flask import Blueprint, render_template, request, redirect, session, flash
from models import  db, Member
from forms import  UserCreateForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash

from lock import login_required

signup_bp= Blueprint('signup',__name__)

@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup_view():
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