from flask import Flask
from models import db
from controllers.employee_bp import employee_bp
from controllers.index_bp import index_bp
from controllers.login_bp import login_bp
from controllers.signup_bp import signup_bp
from controllers.storage_bp import storage_bp

import mysql.connector

app = Flask(__name__)

app.secret_key = '0106'  # 세션 암호화를 위한 시크릿 키 설정 //원래는 config.py에 이 코드 보관

# MySQL 데이터베이스에 직접 연결
connection = mysql.connector.connect(
    host='10.1.3.246',
    user='user6',
    password='1234',
    database='mydb',
    auth_plugin='mysql_native_password'  # 인증 방식 설정
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user6:1234@10.1.3.246/mydb'    #원격 db
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@127.0.0.1/mydb'    #로컬 db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy와 Flask 앱 연동
db.init_app(app)

# 블루프린트 등록
app.register_blueprint(employee_bp)
app.register_blueprint(index_bp)
app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(storage_bp)



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
