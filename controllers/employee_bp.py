from flask import Blueprint, render_template, request, redirect, session, flash
from models import Employee, db, Member
from forms import LoginForm, UserCreateForm, EmployeeCreateForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, get_flashed_messages




from lock import login_required



employee_bp= Blueprint('employee',__name__)


@employee_bp.route('/employee', methods=['GET', 'POST'])
@login_required
def employee_view():
    if request.method == 'GET':
        employees = Employee.query.all()
        return render_template('employee.html', employees=employees)
    elif request.method == 'POST':
        emp_name = request.form.get('name')
        emp_add = request.form.get('region')
        emp_department = request.form.get('department')
        emp_position = request.form.get('position')
        emp_phone = request.form.get('phone')
        emp_email = request.form.get('email')

        new_employee = Employee(
            employee_name=emp_name, employee_address=emp_add,
            employee_department=emp_department, employee_position=emp_position,
            employee_phone=emp_phone, employee_email=emp_email
        )

        db.session.add(new_employee)
        db.session.commit()
        return redirect('/employee')
