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
        # 이미지를 선택하고 imgname에 저장
        imgname = select_image()
        
        if imgname:
            # 선택된 이미지 이름을 사용해 데이터 조회
            image_data = get_image_data(imgname)
        else:
            print("이미지를 선택하지 않았습니다.")

    return render_template('analysis.html', image_data=image_data)
def select_image():
    root = tk.Tk()
    root.withdraw()  # Tkinter 윈도우를 숨김
    img_path = filedialog.askopenfilename(title="이미지 선택", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    
    imgname = None  # 이미지 이름 초기화
    if img_path:
        imgname = os.path.basename(img_path)  # 경로에서 파일 이름만 추출
        print(f"선택된 이미지 이름: {imgname}")
    
    return imgname  # 선택된 이미지 이름 반환

# 이미지 데이터를 가져오는 함수와 연결
def main_process():
    # 이미지를 선택하고 imgname에 저장
    imgname = select_image()
    
    if imgname:
        # 선택된 이미지 이름을 사용해 데이터 조회
        image_data = get_image_data(imgname)
        
        if image_data:
            # 조회된 데이터를 처리하거나 출력
            print(f"조회된 데이터: {image_data}")
        else:
            print("해당 이미지에 대한 데이터를 찾을 수 없습니다.")
    else:
        print("이미지를 선택하지 않았습니다.")