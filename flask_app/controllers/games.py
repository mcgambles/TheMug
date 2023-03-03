from flask_app import app
from flask_app import Flask, render_template, request, redirect, session, url_for, flash, bcrypt
from flask_app.models import user, game, signup
from datetime import datetime



@app.route('/game/create', methods=['POST'])
def create_new_game():

    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')

    if not game.Game.validate_form(request.form):
        return redirect('/game/new')

    data = {
        'name': request.form['name'],
        'num_players': request.form['num_players'],
        'start_time': request.form['start_time'],
        'end_time': request.form['end_time'],
        'location': request.form['location'],
        'description': request.form['description'],
        'user_id': session['id']
    }
    game.Game.create_game(data)
    return redirect('/dashboard')


@app.route('/game/new')
def game_new():
    """Display the form to create a new game"""

    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')

    data = { 'id': session['id'] }
    return render_template('new.html', user=user.User.get_user_by_id(data))


@app.route('/dashboard')
def dashboard():
    """Dashboard"""
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')

    data = {
        'id': session['id']
    }

    one_user = user.User.get_user_by_id(data)

    if one_user:
        session['email'] = one_user.email
        session['first_name'] = one_user.first_name
        session['last_name'] = one_user.last_name
        session['phone'] = one_user.phone
    all_games = game.Game.get_all_games()

    print(all_games)
    return render_template('dashboard.html', one_user=one_user, all_games=all_games)


@app.route('/past')
def past_games():
    """Past games"""
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')

    data = {
        'id': session['id']
    }

    one_user = user.User.get_user_by_id(data)
    if one_user:
        session['email'] = one_user.email
        session['first_name'] = one_user.first_name
        session['last_name'] = one_user.last_name
        session['phone'] = one_user.phone

    all_games = game.Game.get_all_past_games()
    print(all_games)
    return render_template('past.html', one_user=one_user, all_games=all_games)

@app.route('/game/show/<int:game_id>')
def game_show_one(game_id):
    """Show the game on a page"""
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')

    data = { 'id': game_id }
    data_user = { 'id': session['id'] }
    return render_template('show.html', one_game=game.Game.get_one_game(data), user=user.User.get_user_by_id(data_user), signups=signup.Signup.get_game_signups(data))

@app.route('/game/show_past/<int:game_id>')
def game_show_past_one(game_id):
    """Show the game on a page"""
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')

    data = { 'id': game_id }
    data_user = { 'id': session['id'] }
    return render_template('show_past.html', one_game=game.Game.get_one_game(data), user=user.User.get_user_by_id(data_user), signups=signup.Signup.get_game_signups(data))

@app.route('/game/edit/<int:game_id>')
def edit_game(game_id):
    """Edit the game"""
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')

    data = { 'id': game_id }
    data_user = { 'id': session['id'] }
    return render_template('edit.html', one_game=game.Game.get_one_game(data), user=user.User.get_user_by_id(data_user))

@app.route('/game/update', methods=['POST'])
def update_game():
    """Update game after editing"""

    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    if not game.Game.validate_form(request.form):
        id = int(request.form['id'])
        return redirect(f'/game/edit/{id}')

    data = {
        'id': int(request.form['id']),
        'name': request.form['name'],
        'num_players': request.form['num_players'],
        'start_time': request.form['start_time'],
        'end_time': request.form['end_time'],
        'location': request.form['location'],
        'description': request.form['description'],
        'user_id': session['id']
    }

    game.Game.update_game(data)
    id = request.form['id']

    flash("Edit was successful", "success")
    return redirect(f'/game/edit/{id}')

@app.route('/game/delete/<int:game_id>', methods=['POST'])
def delete_game(game_id):
    """Delete game if session user created"""
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')

    data = { 'id': game_id }
    
    game.Game.delete_game(data)
    return redirect('/dashboard')

