from flask import Blueprint, render_template, request, redirect
from models import db, Member
from lock import login_required
from ..forms import UserCreateForm

bp= Blueprint('main',__name__,url_prefix='/')



@bp.route('/signup', methods=['GET', 'POST'])
def signup_view():
    form = UserCreateForm()

    if request.method == 'GET':
        return render_template("signup.html",form=form)
    elif request.method == 'POST':
        if not (userid and password and password_2 and username and userphone and useremail and useradd and userposition):
            return "입력되지 않은 정보가 있습니다"
        elif password != password_2:
            return "비밀번호가 일치하지 않습니다"
        else:
            new_user = Member(
                member_id=userid, member_password=password, member_name=username,
                member_phone=userphone, member_email=useremail, member_address=useradd,
                member_position=userposition
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')