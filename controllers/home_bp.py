from flask import Blueprint, render_template


from lock import login_required

home_bp= Blueprint('home',__name__)

@home_bp.route('/')
@login_required
def storage_view():
        return render_template('basic.html')