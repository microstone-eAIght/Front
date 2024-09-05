from functools import wraps
from flask import redirect, session, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:  # 세션에 로그인 정보가 없으면
            return redirect(url_for('login_view'))  # 로그인 페이지로 리다이렉트
        return f(*args, **kwargs)
    return decorated_function
