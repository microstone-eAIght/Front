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

# 직원 정보 POST (등록)
@admin_bp.route('/admin', methods=['POST'])
@login_required
# 직원 추가
def add_employee():
    employee_name = request.form['employee_name']
    employee_address = request.form['employee_address']
    employee_department = request.form['employee_department']
    employee_position = request.form['employee_position']
    employee_phone = request.form['employee_phone']
    employee_email = request.form['employee_email']
    employee_status = request.form['employee_status']
    emergency_contact = request.form['emergency_contact']
    date_of_birth = request.form['date_of_birth']
    hire_date = request.form['hire_date']
    gender = request.form['gender']

    conn = get_db_connection()
    cursor = conn.cursor()

    # 직원 정보 삽입
    cursor.execute(''' 
        INSERT INTO employee (employee_name, employee_address, employee_department, employee_position, 
                              employee_phone, employee_email, employee_status, emergency_contact, 
                              date_of_birth, hire_date, gender)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (employee_name, employee_address, employee_department, employee_position,
          employee_phone, employee_email, employee_status, emergency_contact,
          date_of_birth, hire_date, gender))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin.admin_view'))
