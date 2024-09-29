import mysql.connector
from flask import session
from werkzeug.security import check_password_hash

# # 데이터베이스 연결 설정
# db_config = {
#     'host': '10.1.3.246',
#     'user': 'user6',
#     'password': '1234',
#     'database': 'mydb',
#     'auth_plugin': 'mysql_native_password'
# }

# 데이터베이스 연결 설정
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '1234',
    'database': 'mydb',
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
        query = "SELECT member_name FROM member WHERE userid = %s"
        cursor.execute(query, (userid,))

        # 첫 번째 결과를 가져옴
        result = cursor.fetchone()

        # 결과가 존재하면 이름을 반환, 그렇지 않으면 None 반환
        if result:
            return result['username']
        else:
            return None

    finally:
        # 커서와 연결을 닫음
        cursor.close()
        conn.close()
    
