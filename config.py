import os

class Config:
    SECRET_KEY = '1234'  # 비밀 키
    DB_HOST = '127.0.0.1'
    DB_USER = 'root'
    DB_PASSWORD = '1234'
    DB_NAME = 'mydb'

# 원격 데이터베이스 연결
# class Config:
#     SECRET_KEY = '1234'  # 비밀 키
#     DB_HOST = '10.1.3.246'
#     DB_USER = 'user6'
#     DB_PASSWORD = '1234'
#     DB_NAME = 'mydb'