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



recent_img_bp= Blueprint('recent_img',__name__)

# 10개의 최근 이미지를 risk 폴더에서 가져오는 API
@recent_img_bp.route('/get_recent_images', methods=['GET'])
def get_recent_images():
    image_folder = 'risk'  # 이미지가 저장된 risk 폴더 경로
    image_files = sorted(
        [img for img in os.listdir(image_folder) if img.endswith(('png', 'jpg', 'jpeg'))],
        key=lambda x: os.path.getmtime(os.path.join(image_folder, x)),
        reverse=True
    )[:10]  # 최근 10개의 이미지 가져오기

    image_urls = [f'/risk/{img}' for img in image_files]  # 각 이미지를 URL로 변환
    return jsonify({'images': image_urls})  # JSON 형식으로 반환

# risk 폴더에서 이미지 파일을 제공하는 API
@recent_img_bp.route('/risk/<filename>')
def serve_image(filename):
    return send_from_directory('risk', filename)