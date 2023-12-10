from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from . import dbase
from .dbmodels import User
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, login_required, logout_user, current_user

# Initialising the name for this file which is 'authentication'
authentication = Blueprint('authentication', __name__)


# Route to Log In Page
@authentication.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        student = request.form.get('student')
        password = request.form.get('password')

        username = User.query.filter_by(student=student).first()

        if username:
            if check_password_hash(username.password, password):
                flash("Logged in successfully", category='success')
                login_user(username, remember=True)
                return redirect(url_for('userview.homepage'))
            else:
                flash("Incorrect password, please try again", category='error')

        else:
            flash("Student ID does not exist", category='error')

    return render_template('login.html', username=current_user)


# Route to Log Out Page
@authentication.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('authentication.login'))


# Route to Register Page
@authentication.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        student = request.form.get('student')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Checks if entered value is valid
        username = User.query.filter_by(student=student).first()
        if username:
            flash('Student ID already exists', category='error')
        elif len(student) < 6:
            flash("Student ID must be more than 6 numbers", category='error')
        elif len(name) < 2:
            flash("Name must be greater than 1 character", category='error')
        elif password1 != password2:
            flash("Password Don't Match", category='error')
        elif len(password1) < 5:
            flash("Password must be at least 5 characters", category='error')
        else:
            try:
                student = int(student)
            except ValueError:
                flash("Student ID must be a valid integer", category='error')
                return render_template('register.html')

            new_user = User(student=student, name=name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            dbase.session.add(new_user)
            dbase.session.commit()
            login_user(new_user, remember=True)
            try:
                dbase.session.commit()
                session['student_id'] = student
                flash("Account Created", category='success')
                return redirect(url_for('userview.homepage'))
            except IntegrityError:
                dbase.session.rollback()
                flash("Student ID already exists", category='error')
                return render_template('register.html')

    return render_template('register.html', username=current_user)

