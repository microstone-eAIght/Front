from flask import Blueprint, render_template
from lock import login_required


admin_bp= Blueprint('admin',__name__)

@admin_bp.route('/admin')
@login_required
def admin_view():
    return render_template('admin.html')