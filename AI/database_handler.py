import pymysql

def save_to_database(image_payload):
    # MySQL 데이터베이스 연결
    connection = pymysql.connect(
        host='localhost',            # 데이터베이스 호스트
        user='root',        # 데이터베이스 사용자
        password='1234',    # 사용자 비밀번호
        db='mydb',          # 데이터베이스 이름
        charset='utf8mb4',           # 문자셋
        cursorclass=pymysql.cursors.DictCursor
    )

    # SQL 쿼리 작성
    sql = """
    INSERT INTO reba_scores 
    (frame_title, reba_score_a, neck_score, trunk_score, leg_score, 
    reba_score_b, shoulder_to_elbow, elbow_to_wrist, wrist_score, reba_score_c, 
    caption, owas_score, trunk_part, arms_part, legs_part, load_part) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    # 데이터 준비 (리스트에서 부분 점수 추출)
    data = (
        image_payload['frame_title'],
        image_payload['reba_score_a'],
        image_payload['partial_a'][0],   # 목 점수
        image_payload['partial_a'][1],   # 몸통 점수
        image_payload['partial_a'][2],   # 다리 점수
        image_payload['reba_score_b'],
        image_payload['partial_b'][0],   # 어깨에서 팔꿈치까지 점수
        image_payload['partial_b'][1],   # 팔꿈치에서 손목까지 점수
        image_payload['partial_b'][2],   # 손목 점수
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

    finally:
        connection.close()  # 연결 종료
