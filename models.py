import mysql.connector
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from config import Config

# 데이터베이스 연결 설정
db_config = {
    'host': Config.DB_HOST,
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'database': Config.DB_NAME,
    'auth_plugin': 'mysql_native_password'
}

def get_db_connection():
    """데이터베이스 연결을 생성하는 함수"""
    return mysql.connector.connect(**db_config)

def get_all_users():
    """모든 사용자 정보를 가져오는 함수"""
    conn = get_db_connection()  # get_db_connection 함수 사용
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM users")  # SQL 쿼리 실행
    users = cursor.fetchall()  # 결과 가져오기
    
    cursor.close()
    conn.close()
    return users

def insert_user(username, email):
    """새 사용자를 데이터베이스에 삽입하는 함수"""
    conn = get_db_connection()  # get_db_connection 함수 사용
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))
    conn.commit()
    
    cursor.close()
    conn.close()

def check_member_login(userid, password):
    """사용자 아이디와 비밀번호를 확인하는 함수"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 사용자 정보 가져오기
    cursor.execute("SELECT * FROM member WHERE member_id = %s", (userid,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user is None:
        # 사용자가 존재하지 않으면 False 반환
        return False

    # 비밀번호가 일치하는지 확인
    if check_password_hash(user['member_password'], password):
        return True
    else:
        return False
    
def get_member_name():
    """세션 userid와 일치하는 첫 번째 사용자의 이름을 가져오는 함수"""
    userid = session.get('user_id')  # 세션에서 user_id를 가져옴

    if userid is None:
        return None  # 세션에 user_id가 없으면 None 반환

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # SQL 쿼리 작성
        query = "SELECT member_name FROM member WHERE member_id = %s"
        cursor.execute(query, (userid,))

        # 첫 번째 결과를 가져옴
        result = cursor.fetchone()

        # 결과가 존재하면 이름을 반환, 그렇지 않으면 None 반환
        if result:
            return result['member_name']
        else:
            return None

    finally:
        # 커서와 연결을 닫음
        cursor.close()
        conn.close()

def check_username_exists(userid):
    """아이디 중복 확인 함수"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM member WHERE member_id = %s"
    cursor.execute(query, (userid,))
    
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return result is not None  # 아이디가 이미 존재하면 True 반환

def insert_member(user_data):
    """회원 정보를 데이터베이스에 삽입하는 함수"""
    conn = get_db_connection()  # 데이터베이스 연결
    cursor = conn.cursor()

    # 비밀번호를 해시 처리

    # 회원 정보를 삽입하는 SQL 쿼리
    insert_query = """
    INSERT INTO member (member_id, member_name, member_password, member_phone, member_email, member_address, member_position)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    # 데이터 삽입
    cursor.execute(insert_query, (
        user_data['userid'],  # 사용자 ID
        user_data['username'],  # 사용자 이름
        user_data['password'],  # 해시 처리된 비밀번호
        user_data['tel'],  # 전화번호
        user_data['email'],  # 이메일
        user_data['address'],  # 주소
        user_data['position']  # 직책
    ))

    conn.commit()  # 변경사항 커밋
    cursor.close()  # 커서 닫기
    conn.close()  # 연결 닫기

# 회원가입 처리 예시
def register_user(form):
    """form 데이터에서 회원가입 처리"""
    insert_member(form)  # 회원 정보를 데이터베이스에 삽입


    
