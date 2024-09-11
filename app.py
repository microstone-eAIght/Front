import os
from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector

from lock import login_required

app = Flask(__name__)

app.secret_key = '0106'  # 세션 암호화를 위한 시크릿 키 설정
# MySQL 데이터베이스 연결 정보
app.config['MYSQL_HOST'] = '10.1.3.246'
app.config['MYSQL_USER'] = 'user2'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'mydb'

# MySQL 연결 객체 생성
mysql = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

@app.route('/', methods=['GET','POST'])
def login_view():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        # 로그인 처리 코드 추가
        userid = request.form.get('아이디')
        password = request.form.get('비밀번호')
        # 데이터베이스에서 사용자 정보 조회
        cursor = mysql.cursor()
        sql = "SELECT * FROM member WHERE member_id = %s AND member_password = %s"
        values = (userid, password)
        cursor.execute(sql, values)
        user = cursor.fetchone()

        if user:
            #임의적으로 들어가는 것을 방지
            session['logged_in'] = True  # 로그인 상태 저장
            session['userid'] = userid  # 사용자 아이디 저장
            # 로그인 성공 시 처리 코드 추가
            return redirect('/index')
        else:
            return "로그인 실패"
    
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        cursor = mysql.cursor()
        cursor.execute("SELECT member_name FROM member WHERE member_id = %s", (session['userid'],))
        user = cursor.fetchone()
        cursor.close()

        if user:
            member_name = user[0]
        else:
            member_name = '이름 없음'

        return render_template("index.html", member_name=member_name)


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    elif request.method == 'POST':
        # 회원가입 처리 코드 추가
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
            # 데이터베이스에 사용자 정보 저장
            cursor = mysql.cursor()
            sql = "INSERT INTO member (member_id,member_name,member_password,member_phone,member_email,member_address,member_position) VALUES (%s, %s, %s,%s,%s,%s,%s)"
            values = (userid, username, password , userphone, useremail, useradd, userposition)
            cursor.execute(sql, values)
            mysql.commit()
            return redirect('/')  # 회원가입 성공 후 로그인 페이지로 리다이렉트
    
@app.route('/Employee', methods=['GET', 'POST'])
@login_required
def Employee():
    if request.method == 'GET':
        cursor = mysql.cursor()
        cursor.execute("SELECT member_name FROM member WHERE member_id = %s", (session['userid'],))
        user = cursor.fetchone()
        cursor.execute("SELECT * FROM employee")  # employee 테이블의 모든 데이터 선택
        employees = cursor.fetchall()
        cursor.close()

        if user:
            member_name = user[0]
        else:
            member_name = '이름 없음'

        return render_template('employee.html', member_name=member_name, employees=employees)
    elif request.method == 'POST':
        # 직원 추가 처리 코드
        emp_name = request.form.get('name')
        emp_add = request.form.get('region')
        emp_department = request.form.get('department')
        emp_position = request.form.get('position')
        emp_phone = request.form.get('phone')
        emp_email = request.form.get('email')

        if not (emp_name and emp_add and emp_department and emp_position and emp_phone and emp_email):
            return "입력되지 않은 정보가 있습니다"
        else:
            cursor = mysql.cursor()
            sql = "INSERT INTO employee (employee_name, employee_address, employee_department, employee_position, employee_phone, employee_email) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (emp_name, emp_add, emp_department, emp_position, emp_phone, emp_email)
            cursor.execute(sql, values)
            mysql.commit()
            cursor.close()
            return redirect('/Employee')




if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)