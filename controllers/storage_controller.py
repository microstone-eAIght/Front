from flask import Blueprint, render_template, session, redirect

storage_bp = Blueprint('storage', __name__)

@storage_bp.route('/storage')
def storage():
        return render_template('storage.html')  # index.html 페이지로 이동

