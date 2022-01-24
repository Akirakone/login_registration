
from flask_bcrypt import bcrypt
from flask import render_template,flash,redirect,request,session
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

DATABASE = "login"


class User:

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.confirm_password = data["confirm_password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    @staticmethod
    def validate(data):
        is_valid = True
        if len(data["first_name"]) <= 3:
            flash("First name must be at least 3 characters.", "register")
            is_valid = False
        if len(data["last_name"]) <= 3:
            flash("Last name must be at least 3 characters.", "register")
            is_valid = False

        if len(data["email"]) < 2:
            flash("Enter email address", "register")
            is_valid = False
        if not email_regex.match(data["email"]):
            flash("Email already in use, please enter a new email", "register")
        is_valid = False

        if len (data ["password"] )< 8:
            is_valid = False
        if not data["confirm_password"] != data["password"]:
            flash("Passwords don't match", "register")
            is_valid = False
        return is_valid

    @classmethod
    def insert_users(cls, data):
        query = "INSERT INTO users (first_name, last_name, email,password, confirm_password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(confirm_password)s)"
        return connectToMySQL("login_schema").query_db(query, data)


    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email=%(email)s"
        user_db = connectToMySQL("login_schema").query_db(query, data)
        if len(user_db) < 1:
            return False
        return cls(user_db[0])


    @classmethod
    def get_users(cls, data):
        query = "SELECT * FROM users WHERE id=%(users_id)s"
        user_db = connectToMySQL("login_schema").query_db(query, data)
        return cls(user_db[0])
