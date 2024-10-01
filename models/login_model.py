from werkzeug.security import check_password_hash
from models.connect_model import get_db_connection


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