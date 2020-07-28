from flask import render_template, send_from_directory, send_file, redirect, url_for
from flask import request, flash
from app import app, db
from datetime import datetime
import os

from app.models import User
from app.forms import LoginForm
from flask_login import login_required, current_user, logout_user, login_user
import json

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html');

# user registration etc

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
