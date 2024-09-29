from flask import render_template
from flask import Blueprint, render_template, request, redirect, session, flash
from lock import login_required
from models import db, Member
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, get_flashed_messages




admin_bp= Blueprint('admin',__name__)

@admin_bp.route('/admin')
@login_required
def admin_view():
    if request.method == 'GET':
        # 사용자 이름 가져오기
        member = Member.query.filter_by(member_id=session['userid']).first()
        if member:
            member_name = member.member_name
        else:
            member_name = '이름 없음'

        return render_template('admin.html', member_name=member_name)
    # 로그인이 되어 있는지 확인