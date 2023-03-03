from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from flask_app.models import user, game
from datetime import datetime


class Signup:

    db = "mug_db"

    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.game_id = data['game_id']
        self.users_who_signuped = user.User.get_user_by_id({"id": self.user_id})

    @classmethod
    def create_signup(cls, data):
        """Add signup to signup tbl"""
        query = '''INSERT INTO signups (user_id, game_id)
        VALUES (%(user_id)s, %(game_id)s);'''
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_game_signups(cls, data):
        """Get signups based on game id"""
        query = "SELECT * FROM signups WHERE game_id=%(id)s ORDER BY id DESC;"
        results = connectToMySQL(cls.db).query_db(query,data)
        signups = []
        if not results:
            return  signups
        for r in results:
            signups.append(cls(r))
        return signups

    @classmethod
    def delete_signup(cls, data):
        """Delete signup from game; based on user_id"""
        query = '''DELETE FROM signups
        WHERE user_id=%(user_id)s AND game_id=%(game_id)s;'''
        return connectToMySQL(cls.db).query_db(query,data)