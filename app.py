import atexit
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
from processes.porcess_manager import terminate_processes
from AI.database_handler import get_image_data

from flask import Flask, send_from_directory, jsonify #블루프린트 해주삼
import os        #블루프린트 해주삼

app = Flask(__name__)
app.config.from_object(Config)  # Config 클래스에서 설정 불러오기

@app.route('/high_risk_images/<filename>')               #블루프린트 해주삼
def high_risk_images(filename):                           #블루프린트 해주삼
    image_folder = 'C:/video_AI/high_risk_images'
    return send_from_directory(image_folder, filename)

@app.route('/get_recent_images', methods=['GET'])  #블루프린트 해주삼
def get_recent_images():                           
    image_folder = 'C:/video_AI/high_risk_images'
    # 폴더에서 이미지 파일들 (jpg, png 등) 가져오기
    images = [f for f in os.listdir(image_folder) if f.endswith(('jpg', 'png'))]
    # 이미지 파일들을 생성 날짜 순으로 정렬하여 최신 이미지 10개 가져오기
    images = sorted(images, key=lambda x: os.path.getctime(os.path.join(image_folder, x)), reverse=True)
    recent_images = images[:10]  # 최신 10개 이미지 가져오기
    return jsonify({'images': recent_images})

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

# 서버 종료 시 실행 중인 백그라운드 프로세스를 종료
atexit.register(terminate_processes)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)