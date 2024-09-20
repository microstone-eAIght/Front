from flask import Blueprint, render_template


from lock import login_required

storage_bp= Blueprint('storage',__name__)

@storage_bp.route('/storage')
@login_required
def storage_view():
        return render_template('storage.html')