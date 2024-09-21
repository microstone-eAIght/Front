import os

class Config:
    SECRET_KEY = '1234'  # 비밀 키
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234@127.0.0.1/mydb'  # 데이터베이스 URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 불필요한 경고 메시지 방지
