from flask import Blueprint, render_template, request, redirect, session, flash
from models import Employee, db, Member
from forms import LoginForm, UserCreateForm, EmployeeCreateForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, get_flashed_messages
from lock import login_required

from lock import login_required

storage_bp= Blueprint('storage',__name__)

@storage_bp.route('/storage')
@login_required
def storage_view():
        if request.method == 'GET':
        # 사용자 이름 가져오기
                member = Member.query.filter_by(member_id=session['userid']).first()
                if member:
                        member_name = member.member_name
                else:
                        member_name = '이름 없음'

                return render_template('storage.html', member_name=member_name)