from flask import render_template, request, redirect,Blueprint,flash
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user
auth = Blueprint('auth', __name__)


# Login page
@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":
        email1 = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email1).first()
        if user:
            if check_password_hash(user.password, password):

                login_user(user, remember=True)
                flash('You have been logged in successfully!', 'success')
                return redirect('/')
            flash('Invalid username or password. Please try again.', 'error')
    return render_template('login.html')


# Logout page
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


# Register page
@auth.route('/register', methods=['GET', 'POST'])
def register():
    admin = User.query.filter_by(user_type='admin').first()
    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        user_type = request.form["userType"]

        user = User.query.filter_by(email=email).first()
        username = User.query.filter_by(name=name).first()
        if user:
            flash('Email already Exists', category='warning')
        elif username:
            flash('Username already Exists', category='warning')
        elif password1 != password2:
            flash('Enter a same password', category='warning')
        elif len(name) < 5:
            flash('Name should be greater than 4 characters', category='warning')
        else:
            new_user = User(email=email, name=name.title(), password=generate_password_hash(
                password1, method='sha256'), user_type=user_type)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('You are logged in, Account has been created successfully.',
                  category='success')
            return redirect('/')

    return render_template("registration.html", admin=admin)


