from flask import Blueprint, request, render_template

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired

from .models import register_user

authentication = Blueprint('authentication', __name__, \
    template_folder='templates/authentication', static_folder='static')

class AuthForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


@authentication.route('/register', methods=['GET', 'POST'])
def register():
    form = AuthForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            data = {}
            data['fname'] = form.fname.data
            data['lname'] = form.lname.data
            data['email'] = form.email.data
            data['username'] = form.username.data
            data['password'] = form.password.data

            response = register_user(data)

            return f"response: {response}"