import os
from flask import Flask, render_template, jsonify, send_from_directory
import plotly.graph_objects as go
import plotly.io as pio
from flask import Blueprint, render_template

from lock import login_required

analysis_bp= Blueprint('analysis',__name__)




@analysis_bp.route('/analysis')
@login_required
def index():
    return render_template('analysis.html')