import os
from flask import Flask, render_template, jsonify, send_from_directory
import plotly.graph_objects as go
import plotly.io as pio
from flask import Blueprint, render_template, request, redirect, session, flash
from models import Employee, db, Member
from forms import LoginForm, UserCreateForm, EmployeeCreateForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, get_flashed_messages

from lock import login_required

reba_button_bp= Blueprint('reba_button',__name__)


@reba_button_bp.route('/reba_a')
def reba_a():
    categories = ['목', '몸통', '다리']
    scores = [3, 4, 2]
    fig = create_radar_chart(categories, scores, 'REBA A')
    graph_html = pio.to_html(fig, full_html=False)
    return jsonify({'graph_html': graph_html, 'score_a': 9})  # 임의의 값 추가

@reba_button_bp.route('/reba_b')
def reba_b():
    categories = ['팔', '아래 팔', '손목']
    scores = [3, 2, 1]
    fig = create_radar_chart(categories, scores, 'REBA B')
    graph_html = pio.to_html(fig, full_html=False)
    return jsonify({'graph_html': graph_html, 'score_b': 6})  # 임의의 값 추가

@reba_button_bp.route('/reba_c')
def reba_c():
    # 임의의 값으로 score_c 설정 (나중에 DB에서 받아올 수 있음)
    score_c = 8  # 이 값을 동적으로 변경 가능

    # score_c 값에 따라 리스크 레벨 설정
    if score_c == 1:
        risk_level = 'Negligible Risk'
        color = 'green'
    elif 2 <= score_c <= 3:
        risk_level = 'Low Risk'
        color = 'lightgreen'
    elif 4 <= score_c <= 7:
        risk_level = 'Medium Risk'
        color = 'yellow'
    elif 8 <= score_c <= 10:
        risk_level = 'High Risk'
        color = 'orange'
    elif 11 <= score_c <= 12:
        risk_level = 'Very High Risk'
        color = 'red'

    # 게이지 차트 데이터 생성
    fig_data = create_gauge_chart(score_c, 'REBA C')

    return jsonify({
        'fig_data': fig_data, 
        'score_c': score_c, 
        'risk_level': risk_level, 
        'color': color  # 색상 정보도 함께 반환
    })

@reba_button_bp.route('/all_scores')
def all_scores():
    # 임의의 점수 설정
    score_a = 9  # REBA A 점수
    score_b = 6  # REBA B 점수
    score_c = 8  # REBA C 점수

    # 결합된 위험도 (DB에서 가져온 값으로 설정)
    combined_risk = "High Risk"  # 결합된 REBA A와 B의 위험도는 DB에서 제공

    # Risk Level 계산 로직
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

    # REBA C의 게이지 차트를 생성
    fig_data = create_gauge_chart(score_c, 'REBA C')

    # JSON으로 리턴 (REBA A, B, C 점수와 결합된 위험도 포함)
    return jsonify({
        'score_a': score_a,
        'score_b': score_b,
        'score_c': score_c,
        'combined_risk': combined_risk,  # 결합된 점수 DB에서 가져온 값
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
def create_gauge_chart(score_c, title):
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

# OWAS 차트 라우트
@reba_button_bp.route('/owas_chart')
def owas_chart():
    # OWAS 점수 예시 값 (임의 값 사용)
    owas_data = {
        "몸통": 3,  # 1~4 범위
        "팔": 2,  # 1~2 범위
        "다리": 5,  # 1~7 범위
        "하중": 1  # 고정값
    }

    # 막대 그래프 생성
    fig_data = create_bar_chart(owas_data, 'OWAS 점수 분석')

    # OWAS 총 점수에 따른 리스크 레벨 설정 (1~4점)
    total_score = 3  # 임의로 설정
    if total_score == 1:
        risk_level = "Normal risk"
    elif total_score == 2:
        risk_level = "Low risk"
    elif total_score == 3:
        risk_level = "Medium risk"
    else:
        risk_level = "High risk"

    return jsonify({'fig_data': fig_data, 'owas_level': risk_level})