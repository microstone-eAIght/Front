import os
from flask import Flask, render_template, jsonify, send_from_directory
import plotly.graph_objects as go
import plotly.io as pio
from flask import Blueprint, request
from controllers.analysis_bp import get_reba_scores

reba_button_bp= Blueprint('reba_button',__name__)


@reba_button_bp.route('/reba_a')
def reba_a():
    # frame_title을 요청에서 가져오거나 필요에 따라 설정합니다.
    frame_title = request.args.get('frame_title')  # 클라이언트 요청에서 가져오기
    print("레바a에서 가져올 수 잇나?:", frame_title)  # 요청된 프레임 제목 출력
    # get_reba_scores 함수를 호출하여 해당 frame_title에 대한 점수 데이터 가져오기
    scores_data = get_reba_scores(frame_title, score_type='A')

    # 카테고리 및 점수 설정
    categories = ['목', '몸통', '다리']  # 필요한 카테고리
    scores = [
        scores_data['neck_score'],  # neck_score 값을 가져옵니다.
        scores_data['trunk_score'],  # trunk_score 값을 가져옵니다.
        scores_data['leg_score']      # leg_score 값을 가져옵니다.
    ]

    # 레이더 차트 생성
    fig = create_radar_chart(categories, scores, 'REBA A')
    graph_html = pio.to_html(fig, full_html=False)

    return jsonify({'graph_html': graph_html, 'score_a': scores_data['reba_score_a']})  # REBA A 점수 포함

@reba_button_bp.route('/reba_b')
def reba_b():
    # frame_title을 요청에서 가져오거나 필요에 따라 설정합니다.
    frame_title = request.args.get('frame_title')  # 클라이언트 요청에서 가져오기
    # get_reba_scores 함수를 호출하여 해당 frame_title에 대한 점수 데이터 가져오기
    scores_data = get_reba_scores(frame_title, score_type='B')

    # 카테고리 및 점수 설정
    categories = ['팔', '아래 팔', '손목']  # 필요한 카테고리
    scores = [
        scores_data['shoulder_to_elbow'],  # 어깨에서 팔꿈치까지 점수 가져오기
        scores_data['elbow_to_wrist'],      # 팔꿈치에서 손목까지 점수 가져오기
        scores_data['wrist_score']          # 손목 점수 가져오기
    ]

    # 레이더 차트 생성
    fig = create_radar_chart(categories, scores, 'REBA B')
    graph_html = pio.to_html(fig, full_html=False)

    return jsonify({'graph_html': graph_html, 'score_b': scores_data['reba_score_b']})  # REBA B 점수 포함


@reba_button_bp.route('/reba_c')
def reba_c():
    # frame_title을 요청에서 가져오거나 필요에 따라 설정합니다.
    frame_title = request.args.get('frame_title')  # 클라이언트 요청에서 가져오기

    # get_reba_scores 함수를 호출하여 해당 frame_title에 대한 점수 데이터 가져오기
    scores_data = get_reba_scores(frame_title, score_type='C')

    # score_c 값을 reba_score_c로 설정
    score_c = scores_data.get('reba_score_c', 0)  # 기본값으로 0 사용

    # 리스크 레벨 및 색상 초기화
    risk_level = "Unknown Risk"  # 기본값 설정
    bar_color = "grey"  # 기본값 설정

    # score_c 값에 따라 리스크 레벨 및 색상 설정
    if score_c == 1:
        risk_level = 'Negligible Risk'
        bar_color = 'green'
    elif 2 <= score_c <= 3:
        risk_level = 'Low Risk'
        bar_color = 'lightgreen'
    elif 4 <= score_c <= 7:
        risk_level = 'Medium Risk'
        bar_color = 'yellow'
    elif 8 <= score_c <= 10:
        risk_level = 'High Risk'
        bar_color = 'orange'
    elif 11 <= score_c <= 12:
        risk_level = 'Very High Risk'
        bar_color = 'red'

    # 게이지 차트 데이터 생성
    fig_data = create_gauge_chart(score_c, 'REBA C', bar_color)

    return jsonify({
        'fig_data': fig_data, 
        'score_c': score_c, 
        'risk_level': risk_level, 
        'color': bar_color  # 색상 정보도 함께 반환
    })


@reba_button_bp.route('/all_scores')
def all_scores():
    frame_title = request.args.get('frame_title')  # 클라이언트 요청에서 가져오기

    # 각 스코어 가져오기
    scores_data_a = get_reba_scores(frame_title, score_type='A')
    score_a = scores_data_a['reba_score_a']
    
    scores_data_b = get_reba_scores(frame_title, score_type='B')
    score_b = scores_data_b['reba_score_b']
    
    scores_data_c = get_reba_scores(frame_title, score_type='C')
    score_c = scores_data_c['reba_score_c']

    combined_risk = "High Risk"  # 예시값

    # Risk Level 계산
    if score_c == 1:
        risk_level = 'Negligible Risk'
    elif 2 <= score_c <= 3:
        risk_level = 'Low Risk'
    elif 4 <= score_c <= 7:
        risk_level = 'Medium Risk'
    elif 8 <= score_c <= 10:
        risk_level = 'High Risk'
    elif 11 <= score_c <= 12:
        risk_level = 'Very High Risk'

    # 바 색상 설정 (예시)
    bar_color = 'green' if score_c <= 3 else 'orange' if score_c <= 7 else 'red'

    # 게이지 차트 데이터 생성
    fig_data = create_gauge_chart(score_c, 'REBA C', bar_color)  # bar_color를 세 번째 인자로 사용

    return jsonify({
        'score_a': score_a,
        'score_b': score_b,
        'score_c': score_c,
        'combined_risk': combined_risk,
        'risk_level': risk_level,
        'fig_data': fig_data
    })


# 레이더 차트 생성 함수
def create_radar_chart(categories, scores, title):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        name=title,
        line=dict(color='rgba(255, 255, 255, 1)', width=2),
        fillcolor='rgba(0, 123, 255, 0.3)',
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0, 0, 0, 0)',
            radialaxis=dict(visible=True, range=[0, 5], gridcolor='rgba(255, 255, 255, 1)', linecolor='rgba(255, 255, 255, 1)'),
            angularaxis=dict(showline=True, linewidth=2, linecolor="rgba(255, 255, 255, 1)")
        ),
        showlegend=False,
        title=dict(text=f'<span class="reba-text">{title}</span>', x=0.5, font=dict(size=24, color='white'), xanchor='center'),
        width=300,
        height=300,
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color="white")
    )
    return fig

# 게이지 차트 생성 함수
def create_gauge_chart(score_c, title, bar_color):
    # score_c 값에 따라 색상 결정 로직
    if score_c == 1:
        bar_color = 'rgba(0, 255, 0, 0.7)'
    elif 2 <= score_c <= 3:
        bar_color = 'rgba(144, 238, 144, 0.7)'
    elif 4 <= score_c <= 7:
        bar_color = 'rgba(255, 255, 0, 0.7)'
    elif 8 <= score_c <= 10:
        bar_color = 'rgba(255, 165, 0, 0.7)'
    elif 11 <= score_c <= 12:
        bar_color = 'rgba(255, 0, 0, 0.7)'

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score_c,
        title={'text': title, 'font': {'size': 24, 'color': 'white'}},
        number={'font': {'color': 'white', 'size': 24}},
        gauge={
            'axis': {'range': [1, 12], 'tickwidth': 2, 'tickcolor': "white", 'tickmode': 'linear', 'dtick': 1, 'tickfont': {'color': 'white'}},
            'borderwidth': 2,
            'bordercolor': 'white',
            'bar': {'color': bar_color, 'thickness': 1.0},
            'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': score_c}
        }
    ))

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=320, width=320, margin=dict(t=25, b=25, l=20, r=25))
    return fig.to_dict()

# 막대 그래프 생성 함수
def create_bar_chart(data, title):
    fig = go.Figure()

    # 몸통 색상 결정
    body_color = 'green' if data["몸통"] == 1 else (
        'lightgreen' if data["몸통"] == 2 else (
            'orange' if data["몸통"] == 3 else 'red'))

    # 팔 색상 결정
    arm_color = 'lightgreen' if data["팔"] == 1 else 'orange'

    # 다리 색상 결정
    leg_color = 'green' if data["다리"] == 1 else (
        'lightgreen' if 2 <= data["다리"] <= 3 else (
            'yellow' if data["다리"] == 4 else (
                'orange' if 5 <= data["다리"] <= 6 else 'red')))

    # 하중 색상 (고정)
    weight_color = 'green'

    # 막대 그래프 그리기
    fig.add_trace(go.Bar(
        x=["몸통", "팔", "다리", "하중"],
        y=[data["몸통"], data["팔"], data["다리"], data["하중"]],
        marker_color=[body_color, arm_color, leg_color, weight_color]
    ))

    # 그래프 디자인 조정
    fig.update_layout(
        title=title,
        xaxis=dict(title="부위", tickangle=0),  # x축 카테고리의 각도 설정
        yaxis=dict(
            title="Score",
            range=[0, 7],
            title_standoff=15,  # y축 제목과 그래프의 간격을 조정
            automargin=True  # 자동 여백 설정
        ),
        width=300,
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )

    return fig.to_dict()

@reba_button_bp.route('/owas_chart')
def owas_chart():
    # frame_title을 요청에서 가져오거나 필요에 따라 설정합니다.
    frame_title = request.args.get('frame_title')  # 클라이언트 요청에서 가져오기

    # get_reba_scores 함수를 호출하여 해당 frame_title에 대한 OWAS 점수 데이터 가져오기
    owas_data = get_reba_scores(frame_title, score_type='OWAS')  # 'OWAS' 타입으로 데이터 가져오기

    # 점수가 None인 경우 기본값 설정
    if owas_data is None:
        owas_data = {
            "몸통": 0,    # trunk_part 
            "팔": 0,      # arms_part 
            "다리": 0,    # legs_part 
            "하중": 0     # load_part 
        }
    else:
        # owas_data가 None이 아닐 경우, 각 카테고리의 점수를 데이터베이스에서 가져온 값으로 설정
        owas_data = {
            "몸통": owas_data.get('trunk_part', 0),  # trunk_part 점수
            "팔": owas_data.get('arms_part', 0),      # arms_part 점수
            "다리": owas_data.get('legs_part', 0),    # legs_part 점수
            "하중": owas_data.get('load_part', 0)      # load_part 점수
        }

    # 막대 그래프 생성
    fig_data = create_bar_chart(owas_data, 'OWAS 점수 분석')

    # OWAS 총 점수 계산 (각 카테고리의 점수를 합산)
    total_score = sum(owas_data.values())

    # 리스크 레벨 설정
    if total_score == 1:
        risk_level = "Normal risk"
    elif total_score == 2:
        risk_level = "Low risk"
    elif total_score == 3:
        risk_level = "Medium risk"
    else:
        risk_level = "High risk"

    return jsonify({'fig_data': fig_data, 'owas_level': risk_level})

