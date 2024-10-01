from models.connect_model import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

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
    hashed_password = generate_password_hash(user_data['password'])

    # 회원 정보를 삽입하는 SQL 쿼리
    insert_query = """
    INSERT INTO member (member_id, member_name, member_password, member_phone, member_email, member_address, member_position)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    # 데이터 삽입
    cursor.execute(insert_query, (
        user_data['userid'],  # 사용자 ID
        user_data['username'],  # 사용자 이름
        hashed_password,  # 해시 처리된 비밀번호
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