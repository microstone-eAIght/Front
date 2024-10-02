from flask import request

class LoginForm:
    def __init__(self):
        self.userid = request.form.get('아이디')
        self.password = request.form.get('비밀번호')


class UserCreateForm:
    def __init__(self):
        self.userid = request.form.get('id')
        self.password = request.form.get('pw')
        self.password_2 = request.form.get('pw_ch')
        self.username = request.form.get('name')
        self.userphone = request.form.get('tel')
        self.useremail = request.form.get('email')
        self.useradd = request.form.get('address')
        self.userposition = request.form.get('position')

class EmployeeCreateForm:
    def __init__(self):
        self.emp_name = request.form.get('name')
        self.emp_add = request.form.get('region')
        self.emp_department = request.form.get('department')
        self.emp_position = request.form.get('position')
        self.emp_phone = request.form.get('phone')
        self.emp_email = request.form.get('email')
