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


def get_image_data(image_name):
    """특정 frame_title에 대한 데이터를 조회하는 함수"""
    # 데이터베이스 연결 설정
    connection = get_db_connection()
    imgname = image_name  # 이미지 이름을 인수로 받음

    try:
        with connection.cursor() as cursor:
            # frame_title에 해당하는 데이터를 가져오는 쿼리
            query = """
                    SELECT reba_score_a, neck_score, trunk_score, leg_score, 
                           reba_score_b, shoulder_to_elbow, elbow_to_wrist, 
                           wrist_score, reba_score_c, owas_score, 
                           trunk_part, arms_part, legs_part, load_part 
                    FROM reba_scores 
                    WHERE frame_title = %s
                """
            cursor.execute(query, (imgname,))  # imgname을 튜플로 전달
            result = cursor.fetchone()

            if result:
                # 결과를 변수에 저장
                reba_score_a = result[0]
                neck_score = result[1]
                trunk_score = result[2]
                leg_score = result[3]
                reba_score_b = result[4]
                shoulder_to_elbow = result[5]
                elbow_to_wrist = result[6]
                wrist_score = result[7]
                reba_score_c = result[8]
                owas_score = result[9]
                trunk_part = result[10]
                arms_part = result[11]
                legs_part = result[12]
                load_part = result[13]

                # 데이터 반환
                return {
                    "reba_score_a": reba_score_a,
                    "neck_score": neck_score,
                    "trunk_score": trunk_score,
                    "leg_score": leg_score,
                    "reba_score_b": reba_score_b,
                    "shoulder_to_elbow": shoulder_to_elbow,
                    "elbow_to_wrist": elbow_to_wrist,
                    "wrist_score": wrist_score,
                    "reba_score_c": reba_score_c,
                    "owas_score": owas_score,
                    "trunk_part": trunk_part,
                    "arms_part": arms_part,
                    "legs_part": legs_part,
                    "load_part": load_part
                }
            #사용시 image_data = get_image_data(image_name) 이렇게 사용한다
            else:
                print("해당 frame_title에 대한 결과가 없습니다.")
                return None
    except mysql.connector.Error as err:
        print(f"에러 발생: {err}")
        return None
    finally:
        connection.close()  # 데이터베이스 연결 종료
