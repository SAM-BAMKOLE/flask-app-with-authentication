from flask import Blueprint, render_template, request, flash, redirect,  url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    email, password = ("", "")
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successully!", category="success")
                login_user(user, remember=True)
                
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again!", category="error")
        else:
            flash("User with this email does not exist", category="error")



    return render_template("login.html", email=email, password=password)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    username = ""
    email = ""
    password = ""
    confirm_password = ""

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        user_exists = user = User.query.filter_by(email=email).first()
        if user_exists:
                flash("This user already exists, sign in instead !", category="error")
                username = ""
                email = ""
                password = ""
                confirm_password = ""
        elif len(email) < 4:
            flash("Email must be greater than 4 characters", category="error")
        elif len(password) < 4:
            flash("Password must be at least 4 characters", category="error")
        elif confirm_password != password:
            flash("Passwords do not match", category="error")
        else:
            new_user = User(username=username, email=email, password=generate_password_hash(password, method="pbkdf2:sha1"))
            db.session.add(new_user)
            db.session.commit()

            flash("Account created successfully!", category="success")
            username = ""
            email = ""
            password = ""
            confirm_password = ""

            # OR CHOOSE TO LOG USER IN DIRECTLY !
            # login_user(new_user, remember=True)
            # return redirect(url_for("views.home"))

            return redirect(url_for("auth.login"))
        

    return render_template("signup.html", username=username, email=email, password=password, confirm_password=confirm_password)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))