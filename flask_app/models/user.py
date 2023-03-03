from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from datetime import datetime
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"


class User:

    db = "mug_db"

    def __init__(self, data):
        """Model a user"""
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.phone = data['phone']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create_user(cls, data):
        """Add new user to db"""
        query = "INSERT INTO users (first_name, last_name, email, phone, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(phone)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_user_by_id(cls, data):
        """Get the user by id"""
        query = "SELECT * FROM users WHERE id = %(id)s;"
        return cls(connectToMySQL(cls.db).query_db(query, data)[0])

    @classmethod
    def get_user_by_email(cls, data):
        """Get user by email"""
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query, data)

        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_all_users(cls,data):
        """Get all users"""
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query,data)
        all_users = []
        for u in results:
            all_users.append(cls(u))
        return all_users

    @staticmethod
    def validate_registration(user):
            """Validate the add a user form"""
            is_valid = True 
            if len(user['first_name']) < 2:
                flash("The first name must be at least 2 characters.", "danger")
                is_valid = False
            if len(user['last_name']) < 2:
                flash("The last name must be at least 2 characters.", "danger")
                is_valid = False
            
            if len(user['email']) < 7:
                flash("The email must be at least 7 characters.", "danger")
                is_valid = False
            
            query = "SELECT * FROM users WHERE email = %(email)s;"
            data = {
                "email": user['email']
            }
            email_result = connectToMySQL('mug_db').query_db(query, data)

            if len(email_result) >= 1:
                flash("Email is already used. Please sign in or register with different email.", "danger")
                is_valid = False
                return is_valid

            if not EMAIL_REGEX.match(user['email']):
                flash("Email is not valid!", "danger")
                is_valid = False
                return is_valid

            if not user['password'] == user['password2']:
                flash("The password must match and be at least 8 characters long, and contain at least one each of the following: one upper, one lower, one digit and one special character.", "danger")
                is_valid = False
            if not re.match(password_pattern, user['password']):
                flash("The password must match and be at least 8 characters long, and contain at least one each of the following: one upper, one lower, one digit and one special character.", "danger")
                is_valid = False
            return is_valid