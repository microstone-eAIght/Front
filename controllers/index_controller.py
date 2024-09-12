from flask import Blueprint, render_template, session, redirect

index_bp = Blueprint('index', __name__)

@index_bp.route('/index')
def index_view():
    # 로그인이 되어 있는지 확인
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html')  # index.html 페이지로 이동
    else:
        return redirect('/')  # 로그인되지 않은 경우 로그인 페이지로 리다이렉트
