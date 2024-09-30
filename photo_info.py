from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PhotoInfo(db.Model):
    __tablename__ = 'photo_info'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    photo_time = db.Column(db.Time, nullable=False)
    frame_number = db.Column(db.Integer, nullable=False)
    owas_risk_rank = db.Column(db.Enum('Negligible Risk', 'Low Risk', 'Medium Risk', 'High Risk', 'Very High Risk'), nullable=False)
    reba_risk_rank = db.Column(db.Enum('Negligible Risk', 'Low Risk', 'Medium Risk', 'High Risk', 'Very High Risk'), nullable=False)

