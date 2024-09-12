from flask import Flask
from models import db
from controllers.login_controller import login_bp
from controllers.signup_controller import signup_bp
from controllers.employee_controller import employee_bp
from controllers.index_controller import index_bp
from controllers.storage_controller import storage_bp

app = Flask(__name__)

app.secret_key = '0106'  # 세션 암호화를 위한 시크릿 키 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy와 Flask 앱 연동
db.init_app(app)

# 블루프린트 등록
app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(index_bp)
app.register_blueprint(storage_bp)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
