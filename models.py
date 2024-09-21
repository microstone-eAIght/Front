from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Member(db.Model):
    __tablename__ = 'member'  # 테이블 이름을 명시적으로 설정
    id = db.Column(db.Integer, primary_key=True)  # 자동 증가되는 기본 키
    member_id = db.Column(db.String(255), nullable=False, unique=True)  # 사용자 아이디
    member_password = db.Column(db.String(255), nullable=False)  # 비밀번호
    member_name = db.Column(db.String(255))  # 이름
    member_phone = db.Column(db.String(255))  # 전화번호
    member_email = db.Column(db.String(255))  # 이메일
    member_address = db.Column(db.String(255))  # 주소
    member_position = db.Column(db.String(255))  # 직책

class Employee(db.Model):
    __tablename__ = 'employee'  # 테이블 이름을 명시적으로 지정
    id = db.Column(db.Integer, primary_key=True)  # 기본 키
    employee_name = db.Column(db.String(255), nullable=False)  # 직원 이름
    employee_address = db.Column(db.String(255))  # 주소
    employee_department = db.Column(db.String(255))  # 부서
    employee_position = db.Column(db.String(255))  # 직책
    employee_phone = db.Column(db.String(255))  # 전화번호
    employee_email = db.Column(db.String(255))  # 이메일
