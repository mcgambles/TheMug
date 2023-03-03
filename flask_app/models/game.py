from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from flask_app.models import user
from datetime import datetime


class Game:

    db = "mug_db"

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.num_players = data['num_players']
        self.start_time = data['start_time']
        self.end_time = data['end_time']
        self.location = data['location']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def create_game(cls,data):
        """Create a game"""
        query = "INSERT INTO games (name, num_players, start_time, end_time, location, description, user_id) VALUES (%(name)s, %(num_players)s, %(start_time)s, %(end_time)s, %(location)s, %(description)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all_games(cls):
        """Get all the games in db"""
        query = '''SELECT * FROM games
                JOIN users AS creators ON games.user_id = creators.id
                WHERE games.start_time > current_timestamp()
                ORDER BY games.start_time ASC;'''
        results = connectToMySQL(cls.db).query_db(query)
        all_games = []
        if not results:
            return all_games
        for r in results:
            game = (cls(r))

            user_data = {
                'id': r['creators.id'],
                'first_name': r['first_name'],
                'last_name': r['last_name'],
                'email': r['email'],
                'phone': r['phone'],
                'password': r['password'],
                'created_at': r['creators.created_at'],
                'updated_at': r['creators.updated_at']
            }

            one_user = user.User(user_data)
            game.creator = one_user
            all_games.append(game)
        return all_games

    @classmethod
    def get_all_past_games(cls):
        """Get all the games in db before current date"""
        query = '''SELECT * FROM games
                JOIN users AS creators ON games.user_id = creators.id
                WHERE games.start_time < current_timestamp()
                ORDER BY games.start_time DESC;'''
        results = connectToMySQL(cls.db).query_db(query)
        all_games = []
        if not results:
            return all_games
        for r in results:
            game = (cls(r))

            user_data = {
                'id': r['creators.id'],
                'first_name': r['first_name'],
                'last_name': r['last_name'],
                'email': r['email'],
                'phone': r['phone'],
                'password': r['password'],
                'created_at': r['creators.created_at'],
                'updated_at': r['creators.updated_at']
            }

            one_user = user.User(user_data)
            game.creator = one_user
            all_games.append(game)
        return all_games

    @classmethod
    def get_one_game(cls,data):
        """Get one game to display"""
        query = '''SELECT * FROM games
                JOIN users AS creators ON games.user_id = creators.id
                WHERE games.id = %(id)s;'''
        results = connectToMySQL(cls.db).query_db(query, data)

        if not results:
            return all_games
        for r in results:
            game = (cls(r))

            user_data = {
                'id': r['creators.id'],
                'first_name': r['first_name'],
                'last_name': r['last_name'],
                'email': r['email'],
                'phone': r['phone'],
                'password': r['password'],
                'created_at': r['creators.created_at'],
                'updated_at': r['creators.updated_at']
            }

            one_user = user.User(user_data)
            game.creator = one_user
        return game

    @classmethod
    def update_game(cls,data):
        """Update the game"""
        query = "UPDATE games SET name=%(name)s, num_players=%(num_players)s, start_time=%(start_time)s, end_time=%(end_time)s, location=%(location)s, description=%(description)s  WHERE games.id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def delete_game(cls,data):
        """Delete game"""
        query = "DELETE FROM games WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_form(game):
        """Validate the new game create form"""
        is_valid = True 
        if len(game['name']) < 2:
            flash("The name must be at least 2 characters.", "danger")
            is_valid = False
        if len(game['num_players']) < 1:
            flash("The number of players can not be blank.", "danger")
            is_valid = False
        if len(game['location']) < 5:
            flash("The location must be greater than 5.", "danger")
            is_valid = False
        if len(game['description']) < 15:
            flash("The description must be greater than 15.", "danger")
            is_valid = False
        return is_valid
