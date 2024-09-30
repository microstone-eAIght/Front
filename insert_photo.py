from photo_info import PhotoInfo, db
from datetime import datetime
from flask import Flask
from config import Config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}/{Config.DB_NAME}"
db.init_app(app)

def save_ai_results(ai_results):
    with app.app_context():
        # OWAS 및 REBA 점수 조정
        owas_risk_rank = adjust_owas_rank(ai_results['owas_risk_rank'])
        reba_risk_rank = adjust_reba_rank(ai_results['reba_risk_rank'])

        # AI 결과를 이용해 PhotoInfo 객체 생성
        new_photo = PhotoInfo(
            photo_date=datetime.now().date(),                         # 현재 날짜로 저장
            location=ai_results['location'],                          # AI로부터 받은 장소 정보
            photo_time=datetime.now().time(),                         # 현재 시간으로 저장
            frame_number=ai_results['frame_number'],                  # AI로부터 받은 프레임 번호
            owas_risk_rank=owas_risk_rank,                           # 조정된 OWAS 등급
            reba_risk_rank=reba_risk_rank                            # 조정된 REBA 등급
        )

        # 데이터베이스에 추가
        db.session.add(new_photo)
        db.session.commit()

def adjust_owas_rank(owas_score):
    # 여기서 owas_score를 ENUM 값으로 매핑합니다.
    if owas_score == 'Medium Risk. Further Investigate. Change Soon':
        return 'Medium Risk'
    # 필요한 경우 다른 조건 추가
    return 'Negligible Risk'  # 기본값 설정

def adjust_reba_rank(reba_score):
    # 여기서 reba_score를 ENUM 값으로 매핑합니다.
    if reba_score == 'Medium Risk. Further Investigate. Change Soon':
        return 'Medium Risk'
    # 필요한 경우 다른 조건 추가
    return 'Negligible Risk'  # 기본값 설정
