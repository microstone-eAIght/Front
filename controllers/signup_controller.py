from flask import Blueprint, render_template, request, redirect
from models import db, Member

signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup_controller():
    if request.method == 'GET':
        return render_template("signup.html")
    elif request.method == 'POST':
        userid = request.form.get('id')
        password = request.form.get('pw')
        password_2 = request.form.get('pw_ch')
        username = request.form.get('name')
        userphone = request.form.get('tel')
        useremail = request.form.get('email')
        useradd = request.form.get('address')
        userposition = request.form.get('position')

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
