from flask import session
from models.connect_model import get_db_connection

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
