from flask import Blueprint, render_template, request, redirect
from flask_wtf import FlaskForm

class UserCreateForm(FlaskForm):
    userid = request.form.get('id')
    password = request.form.get('pw')
    password_2 = request.form.get('pw_ch')
    username = request.form.get('name')
    userphone = request.form.get('tel')
    useremail = request.form.get('email')
    useradd = request.form.get('address')
    userposition = request.form.get('position')