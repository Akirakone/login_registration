from flask_app import app
from flask import render_template,flash,redirect,request,session
from flask_app.models.user import User ,bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
import math


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register',methods=['POST'])
def register():
    print("***************************************")
    is_valid = User.validate(request.form)

    if is_valid:
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "confirm_password": request.form["confirm_password"],
            "password": bcrypt.generate_password_hash(request.form["password"])
        }

        users_id = User.save(data)
        session["login_schema"] = users_id
        flash("NewUser created")
        return redirect("/")
    else:
        return redirect("/")

@app.route("/login",methods=["POST"])
def login():
    users_in_db = User.get_by_email(request.form)
    if not users_in_db:
        flash("invalid email/password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(users_in_db.password, request.form["password"]): 
        flash("invalid email/password", "login")
        return redirect("/")
    session["login_schema"] = users_in_db.id   
    return redirect("/yourlogin")

@app.route("/yourlogin")
def successful_login():
    if "login_schema" not in session:
        flash("Log in or register","register")
        return redirect("/")

    return render_template("index.html")
    
@app.route("/logout")
def logout():
    session.clear()
    flash("logged out!", "login")
    return redirect("/")


