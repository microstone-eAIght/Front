import mysql.connector
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