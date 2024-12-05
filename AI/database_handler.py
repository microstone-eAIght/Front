import pymysql
import os
import sys
import mysql.connector
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config


def get_db_connection():
    """데이터베이스 연결을 생성하는 함수"""
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def save_to_database(image_payload):
    """이미지 데이터를 데이터베이스에 저장하는 함수"""
    # 데이터베이스 연결
    connection = get_db_connection()

    # SQL 쿼리 작성
    sql = """
    INSERT INTO reba_scores 
    (frame_title, reba_score_a, neck_score, trunk_score, leg_score, 
    reba_score_b, shoulder_to_elbow, elbow_to_wrist, wrist_score, reba_score_c, 
    caption, owas_score, trunk_part, arms_part, legs_part, load_part) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # 데이터 준비
    data = (
        image_payload['frame_title'],
        image_payload['reba_score_a'],
        image_payload['partial_a'][0],  # 목 점수
        image_payload['partial_a'][1],  # 몸통 점수
        image_payload['partial_a'][2],  # 다리 점수
        image_payload['reba_score_b'],
        image_payload['partial_b'][0],  # 어깨에서 팔꿈치까지 점수
        image_payload['partial_b'][1],  # 팔꿈치에서 손목까지 점수
        image_payload['partial_b'][2],  # 손목 점수
        image_payload['reba_score_c'],
        image_payload['caption'],
        image_payload['owas_score'],
        image_payload['partial_score'][0],  # 몸통 점수
        image_payload['partial_score'][1],  # 팔 점수
        image_payload['partial_score'][2],  # 다리 점수
        image_payload['partial_score'][3]   # 하중 점수
    )

    # 데이터베이스에 삽입
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, data)
        connection.commit()
    except pymysql.MySQLError as err:
        print(f"데이터베이스 오류: {err}")
    finally:
        connection.close()  # 연결 종료


def get_image_data(imgname):
    """이미지 데이터를 데이터베이스에서 가져오는 함수 (REBA 점수 포함)"""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 이미지 이름에 해당하는 데이터 조회 쿼리
            sql = "SELECT * FROM reba_scores WHERE frame_title = %s"
            print(f"Executing query with frame_title: {imgname}")  # 디버깅 출력
            cursor.execute(sql, (imgname,))
            result = cursor.fetchone()
            
            if result is None:
                print(f"No data found for frame_title: {imgname}")  # 결과가 없을 경우 메시지 출력
                return None  # 데이터가 없을 경우 None 반환
            
           
            return result  # 이미지 데이터 및 REBA 점수를 포함하는 데이터 반환
            
    except Exception as e:
        print(f"Error occurred: {e}")  # 예외 발생 시 메시지 출력
        return None  # 예외 발생 시 None 반환
    finally:
        connection.close()

