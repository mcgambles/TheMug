from flask_app import Flask, render_template, request, redirect, session, url_for, flash, bcrypt
from datetime import datetime
from flask_app import app
from re import A
from flask_app.models import user, game


@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def regitster():
    """Register new user"""
    if not user.User.validate_registration(request.form):
        return redirect('/')

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'phone': request.form['phone'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }

    user_id = user.User.create_user(data)

    if user_id:
        session['id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    """Login in the user"""

    data = { 'email': request.form['email'] }
    user_in_db = user.User.get_user_by_email(data)

    if not user_in_db:
        flash("Invalid Email or Need to register", "danger")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']): 
        flash("The password must match and be at least 8 characters, and contain at least one each of the following: one upper, one lower, one digit and one special character.", "danger")
        return redirect('/')

    session['id'] = user_in_db.id 
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    """Logged the user out of seesion and redirect to login"""
    session.clear()
    return redirect('/')