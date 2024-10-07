import os,sys
from flask import Flask, render_template, jsonify, send_from_directory
import plotly.graph_objects as go
import plotly.io as pio
from flask import Blueprint, request
import tkinter as tk
from tkinter import filedialog
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from AI.database_handler import get_image_data,save_to_database
from lock import login_required

analysis_bp= Blueprint('analysis',__name__)




@analysis_bp.route('/analysis', methods=['GET', 'POST'])
@login_required
def index():
    image_data = None
    reba_scores = None  # REBA 점수를 저장할 변수 추가

    if request.method == 'POST':
        imgname = request.form.get('imgname')

        if imgname:
            # 선택된 이미지 이름을 사용해 데이터 조회
            image_data = get_image_data(imgname)
            if image_data:
                # REBA A, B, C 점수 가져오기
                reba_scores = {
                    'reba_a': image_data['reba_score_a'],
                    'reba_b': image_data['reba_score_b'],
                    'reba_c': image_data['reba_score_c']
                }
            else:
                print("해당 이미지 데이터가 없습니다.")
        else:
            print("이미지를 선택하지 않았습니다.")

    return render_template('analysis.html', image_data=image_data, reba_scores=reba_scores)


def get_reba_scores(frame_title, score_type):
    score_data = get_image_data(frame_title)  # 이미지 데이터 가져오기
    print("Score Data:", score_data)  # 가져온 데이터 출력
    
    if score_data is None:
        # 데이터가 없는 경우 기본 값을 설정
        return {
            "reba_score_a": 0,
            "neck_score": 0,
            "trunk_score": 0,
            "leg_score": 0,
            "reba_score_b": 0,
            "shoulder_to_elbow": 0,
            "elbow_to_wrist": 0,
            "wrist_score": 0,
            "reba_score_c": 0,
            "owas_score": 0,
            "trunk_part": 0,
            "arms_part": 0,
            "legs_part": 0,
            "load_part": 0,
        }
    
    # score_data에서 필요한 점수 추출
    data = {
        "reba_score_a": score_data.get('reba_score_a', 0),  
        "neck_score": score_data.get('neck_score', 0),      
        "trunk_score": score_data.get('trunk_score', 0),    
        "leg_score": score_data.get('leg_score', 0),        
        "reba_score_b": score_data.get('reba_score_b', 0),
        "shoulder_to_elbow": score_data.get('shoulder_to_elbow', 0),
        "elbow_to_wrist": score_data.get('elbow_to_wrist', 0),
        "wrist_score": score_data.get('wrist_score', 0),
        "reba_score_c": score_data.get('reba_score_c', 0),
        "owas_score": score_data.get('owas_score', 0),
        "trunk_part": score_data.get('trunk_part', 0),
        "arms_part": score_data.get('arms_part', 0),
        "legs_part": score_data.get('legs_part', 0),
        "load_part": score_data.get('load_part', 0),
    }
    return data  # dict 형태로 반환

@analysis_bp.route('/get_reba_scores')
def get_reba_scores_api():
    frame_title = request.args.get('frame_title')
    score_type = request.args.get('type')

    scores = get_reba_scores(frame_title, score_type)
    return jsonify(scores)  # 이제 scores는 dict이므로 jsonify로 변환할 수 있습니다.