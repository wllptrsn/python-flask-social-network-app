import json
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# A blueprint of an application means that it stores your urls
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in Successfully!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('posts.home'))
            else:
                flash('Incorrect password. Try again', category="error")
        else:
            flash('Email does not exist. Please try again.', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = Users.query.filter_by(email=email).first()
        userExists = Users.query.filter_by(username=username).first()
        if user:
            flash('Email already exists', category='error')
        if userExists:
            flash('Username already exists. Please pick a new one.', category='error')
        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First Name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = Users(email=email, first_name=first_name, last_name=last_name, username=username, password=generate_password_hash(
                password1, method='sha256'))

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            flash('Account Created!', category='success')

            return redirect(url_for('profiles.createProfile'))
    return render_template("signup.html", user=current_user)
