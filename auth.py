from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = generate_password_hash("admin123")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD, password):
            session["admin"] = True
            return redirect("/admin")

    return render_template("login.html")

@auth.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")