from models.connect_model import get_db_connection
from datetime import datetime  # datetime 모듈 임포트

def save_scores(result_data):
    """점수 데이터를 데이터베이스에 저장하는 함수"""

    # 데이터베이스 연결
    conn = get_db_connection()  
    cursor = conn.cursor()

    # INSERT 쿼리
    try:
        insert_query = """
        INSERT INTO photo_info (
            photo_date, location, photo_time, frame_number, 
            reba_a_total, reba_a_neck, reba_a_trunk, reba_a_leg, 
            reba_b_total, reba_b_upper_arm, reba_b_lower_arm, reba_b_load, 
            reba_c_total, reba_c_risk_level, owas_total, 
            owas_trunk, owas_arm, owas_leg, owas_load, 
            owas_risk_rank, reba_risk_rank
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        data_values = (
            result_data['photo_date'], 
            result_data['location'], 
            result_data['photo_time'], 
            result_data['frame_number'], 
            result_data['reba_a_total'], 
            result_data['reba_a_neck'], 
            result_data['reba_a_trunk'], 
            result_data['reba_a_leg'], 
            result_data['reba_b_total'], 
            result_data['reba_b_upper_arm'], 
            result_data['reba_b_lower_arm'], 
            result_data['reba_b_load'], 
            result_data['reba_c_total'], 
            result_data['reba_c_risk_level'], 
            result_data['owas_total'], 
            result_data['owas_trunk'], 
            result_data['owas_arm'], 
            result_data['owas_leg'], 
            result_data['owas_load'], 
            result_data['owas_risk_rank'], 
            result_data['reba_risk_rank']
        )
        
        # 데이터 삽입
        cursor.execute(insert_query, data_values)
        conn.commit()
    except Exception as e:
        print(f"Error saving scores: {e}, Data: {data_values}")  # 오류 메시지 출력
    finally:
        cursor.close()
        conn.close()

def save_ai_results(ai_results):
    """AI 결과를 저장하는 함수"""
    # OWAS 및 REBA 점수 조정
    owas_risk_rank = adjust_owas_rank(ai_results['owas_risk_rank'])
    reba_risk_rank = adjust_reba_rank(ai_results['reba_risk_rank'])

    # result_data 딕셔너리 생성
    result_data = {
        'photo_date': datetime.now().date(),   # 현재 날짜
        'location': ai_results['location'],     # AI로부터 받은 장소 정보
        'photo_time': datetime.now().time(),    # 현재 시간
        'frame_number': ai_results['frame_number'],  # AI로부터 받은 프레임 번호
        'reba_a_total': ai_results['reba_a_total'],  # REBA A 총점
        'reba_a_neck': ai_results['reba_a_neck'],    # REBA A 목 점수
        'reba_a_trunk': ai_results['reba_a_trunk'],  # REBA A 몸통 점수
        'reba_a_leg': ai_results['reba_a_leg'],      # REBA A 다리 점수
        'reba_b_total': ai_results['reba_b_total'],  # REBA B 총점
        'reba_b_upper_arm': ai_results['reba_b_upper_arm'],  # REBA B 위팔 점수
        'reba_b_lower_arm': ai_results['reba_b_lower_arm'],  # REBA B 아래팔 점수
        'reba_b_load': ai_results['reba_b_load'],    # REBA B 하중 점수
        'reba_c_total': ai_results['reba_c_total'],   # REBA C 총점
        'reba_c_risk_level': ai_results['reba_c_risk_level'],  # REBA C 위험도 (고정 값)
        'owas_total': ai_results['owas_total'],      # OWAS 총점
        'owas_trunk': ai_results['owas_trunk'],      # OWAS 허리 점수
        'owas_arm': ai_results['owas_arm'],          # OWAS 팔 점수
        'owas_leg': ai_results['owas_leg'],          # OWAS 다리 점수
        'owas_load': ai_results['owas_load'],        # OWAS 하중 점수 (고정 값)
        'owas_risk_rank': owas_risk_rank,            # 조정된 OWAS 위험 등급
        'reba_risk_rank': reba_risk_rank              # 조정된 REBA 위험 등급
    }

    # save_scores 함수 호출
    save_scores(result_data)

def adjust_owas_rank(owas_score):
    """OWAS 점수를 ENUM 값으로 매핑"""
    if owas_score == 'High Risk':
        return 'High Risk'
    elif owas_score == 'Very High Risk':
        return 'Very High Risk'
    elif owas_score == 'Medium Risk. Further Investigate. Change Soon':
        return 'Medium Risk'
    
    return 'Medium Risk'  # 기본값 설정

def adjust_reba_rank(reba_score):
    """REBA 점수를 ENUM 값으로 매핑"""
    if reba_score == 'High Risk':
        return 'High Risk'
    elif reba_score == 'Very High Risk':
        return 'Very High Risk'
    elif reba_score == 'Medium Risk. Further Investigate. Change Soon':
        return 'Medium Risk'
    
    return 'Medium Risk'  # 기본값 설정
