from models.connect_model import get_db_connection

def save_scores(result_data):
    """점수 데이터를 데이터베이스에 저장하는 함수"""

    # 데이터베이스 연결
    conn = get_db_connection()  
    cursor = conn.cursor()

    # INSERT 쿼리
    insert_query = """
    INSERT INTO photo_info (photo_date, location, photo_time, frame_number, owas_risk_rank, reba_risk_rank)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    # result_data에서 필요한 값을 추출
    photo_date = result_data.get('photo_date')
    location = result_data.get('location')
    photo_time = result_data.get('photo_time')
    frame_number = result_data.get('frame_number')
    owas_risk_rank = result_data.get('owas_risk_rank')
    reba_risk_rank = result_data.get('reba_risk_rank')

    # 데이터 삽입
    cursor.execute(insert_query, (
        photo_date,        # 사진 날짜
        location,          # 위치
        photo_time,        # 사진 시간
        frame_number,      # 프레임 번호
        owas_risk_rank,    # OWAS 위험 등급
        reba_risk_rank     # REBA 위험 등급
    ))
    
    # 변경 사항 커밋 및 커서와 연결 종료
    conn.commit()
    cursor.close()
    conn.close()