# app.py
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from photo_info import PhotoInfo
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}/{Config.DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/api/scores', methods=['POST'])
def save_scores():
    data = request.json

    ai_results = {
        'location': data.get('location'),
        'frame_number': data.get('frame_number'),
        'owas_risk_rank': data.get('owas_score'),
        'reba_risk_rank': data.get('reba_score_c')
    }
    
    save_ai_results(ai_results)

    return jsonify({'message': 'Scores saved successfully!'}), 201

def save_ai_results(ai_results):
    with app.app_context():
        new_photo = PhotoInfo(
            photo_date=datetime.now().date(),
            location=ai_results['location'],
            photo_time=datetime.now().time(),
            frame_number=ai_results['frame_number'],
            owas_risk_rank=ai_results['owas_risk_rank'],
            reba_risk_rank=ai_results['reba_risk_rank']
        )

        db.session.add(new_photo)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
