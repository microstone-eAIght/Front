import os,sys
from flask import Flask, render_template, jsonify, send_from_directory
import plotly.graph_objects as go
import plotly.io as pio
from flask import Blueprint, request
import tkinter as tk
from tkinter import filedialog
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from AI.database_handler import get_image_data
from lock import login_required

analysis_bp= Blueprint('analysis',__name__)




@analysis_bp.route('/analysis', methods=['GET', 'POST'])
@login_required
def index():
    image_data = None
    
    if request.method == 'POST':
        # JavaScript에서 전송된 이미지 이름 가져오기
        imgname = request.form.get('imgname')

        if imgname:
            # 선택된 이미지 이름을 사용해 데이터 조회
            image_data = get_image_data(imgname)
        else:
            print("이미지를 선택하지 않았습니다.")

    return render_template('analysis.html', image_data=image_data)
