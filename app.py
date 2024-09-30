from flask import Flask
# from controllers.employee_bp import employee_bp
from controllers.index_bp import index_bp
from controllers.login_bp import login_bp
from controllers.signup_bp import signup_bp
from controllers.storage_bp import storage_bp
from controllers.home_bp import home_bp
from controllers.recent_img_bp import recent_img_bp
from controllers.reba_button_bp import reba_button_bp
from controllers.analysis_bp import analysis_bp
from controllers.admin_bp import admin_bp
from config import Config  # config.py 임포트



app = Flask(__name__)
app.config.from_object(Config)  # Config 클래스에서 설정 불러오기



# 블루프린트 등록
# app.register_blueprint(employee_bp)
app.register_blueprint(index_bp)
app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(storage_bp)
app.register_blueprint(home_bp)
app.register_blueprint(reba_button_bp)
app.register_blueprint(recent_img_bp)
app.register_blueprint(analysis_bp)
app.register_blueprint(admin_bp)



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)