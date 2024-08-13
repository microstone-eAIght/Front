import os  # 디렉토리 절대 경로
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from Models import db
from Models import User

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def login_view():
    if request.method == 'GET':
        return render_template("login.html")
    
@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    
@app.route('/Employee', methods=['GET','POST'])
def Employee():
    if request.method == 'GET':
        return render_template("Employee.html")
    
@app.route('/register', methods=['GET','POST'])  # GET(정보보기), POST(정보수정) 메서드 허용
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        userid = request.form.get('userid')
        email = request.form.get('email')
        password = request.form.get('password')
        password_2 = request.form.get('password_2')

        if not (userid and email and password and password_2):
            return "입력되지 않은 정보가 있습니다"
        elif password != password_2:
            return "비밀번호가 일치하지 않습니다"
        else:
            usertable = User()  # user_table 클래스
            usertable.userid = userid
            usertable.email = email
            usertable.password = password
            
            db.session.add(usertable)
            db.session.commit()
            return redirect('/login')  # 회원가입 성공 후 로그인 페이지로 리다이렉트

if __name__ == "__main__":
    # 데이터베이스 설정
    basedir = os.path.abspath(os.path.dirname(__file__)) 
    dbfile = os.path.join(basedir, 'db.sqlite') 

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    db.init_app(app) 

    # 여기서 애플리케이션 컨텍스트를 설정합니다.
    with app.app_context():  # 추가된 부분
        db.create_all()  # DB 생성

    app.run(host="127.0.0.1", port=5000, debug=True)
