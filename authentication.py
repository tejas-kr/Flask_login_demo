from flask import Blueprint, request, render_template, session, redirect, url_for, current_app

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, InputRequired, ValidationError, Length, Email

import re
from functools import wraps

from .models import register_user, login_user

authentication = Blueprint('authentication', __name__, \
    template_folder='templates/authentication', static_folder='static')

def validate_username(form, field):
    regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')
    if regex.search(field.data) != None:
        raise ValidationError("Only accepted special symbol is '_'")

class RegisterForm(FlaskForm):
    fname = StringField('First Name', validators=[InputRequired()])
    lname = StringField('Last Name', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    username = StringField('Username', [InputRequired(),
                Length(min=8, message="Minimum password length should be %(min)d Characters"), validate_username])
    password = PasswordField('Password', validators=[InputRequired(),
                Length(min=8, message="Minimum password length should be %(min)d Characters")])


class LoginForm(FlaskForm):
    username = StringField('Username', [InputRequired(),
                Length(min=8, message="Minimum password length should be %(min)d Characters"), validate_username])
    password = PasswordField('Password', validators=[InputRequired(),
                Length(min=8, message="Minimum password length should be %(min)d Characters")])


def authentication_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if (not session.get('user_id')) or (not session.get('user_uuid')) or (not session.get('username')):
            return redirect(url_for('authentication.login'))
        return func(*args, **kwargs)
    return wrapper

@authentication.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = {}
        data['fname'] = form.fname.data
        data['lname'] = form.lname.data
        data['email'] = form.email.data
        data['username'] = form.username.data
        data['password'] = form.password.data

        count, result = register_user(data)

        if count == 1:
            return f"User has been registered with username: {result[0]} and UUID: {result[1]}", 201
        return count, 201
    return render_template('register.html', form=form)

@authentication.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = {}
        data['username'] = form.username.data
        data['password'] = form.password.data

        count, result = login_user(data)

        if (count == 1) and (result[0][-1] == data['username']):
            session['user_id'] = result[0][0]
            session['user_uuid'] = result[0][1]
            session['username'] = result[0][2]
            return redirect(url_for('show_data.data'))
        else: 
            current_app.logger.error("Wrong username or password")
            return "Wrong username or password", 401

    if session.get('user_id') and session.get('user_uuid') and session.get('username'):
        return redirect(url_for('show_data.data'))
    
    return render_template('login.html', form=form)

@authentication.route('/logout', methods=['GET'])
@authentication_required
def logout():
    session.pop('user_id', None)
    session.pop('user_uuid', None)
    session.pop('username', None)
    return redirect(url_for('authentication.login'))
