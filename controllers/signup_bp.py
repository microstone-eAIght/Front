from flask import Blueprint, render_template, request, redirect, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import check_username_exists, insert_member


signup_bp= Blueprint('signup',__name__)


@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # 폼에서 입력된 값들 가져오기
        userid = request.form['userid']  # 아이디
        password = request.form['password']  # 비밀번호
        password_ch = request.form['password_ch']  # 비밀번호 확인
        username = request.form['username']  # 이름
        tel = request.form['tel']  # 전화번호
        email = request.form['email']  # 이메일
        address = request.form['address']  # 주소
        position = request.form['position']  # 직책

        # 1. 비밀번호 일치 여부 확인
        if password != password_ch:
            flash('비밀번호가 일치하지 않습니다.', 'error')
            return redirect('/signup')

        # 2. 비밀번호 해시화
        hashed_password = generate_password_hash(password)

        # 3. 사용자 데이터베이스에 저장
        user_data = {
            'userid': userid,
            'username': username,
            'password': hashed_password,
            'tel': tel,
            'email': email,
            'address': address,
            'position': position
        }
        insert_member(user_data)  # 데이터베이스에 삽입

        flash('회원가입이 완료되었습니다.', 'success')
        return redirect('/login')  # 회원가입 완료 후 로그인 페이지로 리다이렉트

    return render_template('signup.html')  # GET 요청일 경우 회원가입 페이지 렌더링


@signup_bp.route('/check_username', methods=['POST'])
def check_username():
    data = request.get_json()
    userid = data.get('userid')

    if check_username_exists(userid):
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False})