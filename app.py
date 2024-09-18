from flask import Flask
from models import db
from views import bp

app = Flask(__name__)

app.secret_key = '0106'  # 세션 암호화를 위한 시크릿 키 설정 //원래는 config.py에 이 코드 보관
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy와 Flask 앱 연동
db.init_app(app)

# 블루프린트 등록
app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
