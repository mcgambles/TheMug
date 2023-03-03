from flask_app import app
from flask_app import Flask, render_template, request, redirect, session, url_for, flash, bcrypt
from datetime import datetime
from flask_app.models import user, game, signup

@app.route('/signup', methods=['POST'])
def add_signup_game():
    """Add a signup to the game"""

    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    signup.Signup.create_signup(request.form)
    return redirect(f"/game/show/{request.form['game_id']}")

@app.route('/signup/delete', methods=['POST'])
def gae_delete_signup():
    """Delete the users signup from game"""

    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    signup.Signup.delete_signup(request.form)
    return redirect(f"/game/show/{request.form['game_id']}")