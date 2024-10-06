from flask import Blueprint, render_template, session




home_bp= Blueprint('home',__name__)

@home_bp.route('/')

def home_view():

        session.pop('_flashes', None)
        return render_template('home.html')