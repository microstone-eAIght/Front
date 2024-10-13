from flask import Blueprint, render_template, request, redirect, url_for,session
from lock import login_required
from models.connect_model import get_db_connection
from models.index_model import get_member_name
# Blueprint 정의
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin', methods=['GET'])
@login_required
def admin_view():
    # 데이터베이스 연결
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 모든 회원 정보를 조회
    cursor.execute('SELECT id, member_name, member_address, member_position, member_phone, member_email FROM member')
    members = cursor.fetchall()

    # 사용자 이름 가져오기 (예: 세션에서 가져옴)
    member_name = get_member_name()

    # 커서와 연결 종료
    cursor.close()
    conn.close()

    # members와 member_name 변수를 함께 전달
    return render_template('admin.html', members=members, member_name=member_name)

# 회원 정보 POST (등록)
@admin_bp.route('/admin', methods=['POST'])
@login_required
#직원추가
def add_member():
    member_id = request.form['member_id']
    member_name = request.form['member_name']
    member_password = request.form['member_password']
    member_phone = request.form['member_phone']
    member_email = request.form['member_email']
    member_address = request.form['member_address']
    member_position = request.form['member_position']

    conn = get_db_connection()
    cursor = conn.cursor()

    # 회원 정보 삽입
    cursor.execute(''' 
        INSERT INTO member (member_id, member_name, member_password, member_phone, member_email, member_address, member_position)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (member_id, member_name, member_password, member_phone, member_email, member_address, member_position))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin.admin_view'))
