from flask import Blueprint, redirect, render_template, request, session
from helpers import apology
from werkzeug.security import check_password_hash

import sqlite3

login_bp = Blueprint('login', __name__)


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        connection = sqlite3.connect("calendar.db")
        cursor = connection.cursor()

        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("username required. please enter a username.")

        if not password:
            return apology("password required. please enter a password.")

        users_with_same_username = cursor.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchall()

        if len(users_with_same_username) != 1:
            return apology("username does not exist. please check and try again.", 404)

        user = users_with_same_username[0]

        if not check_password_hash(user[2], password):
            return apology(
                "provided password is incorrect. please check and try again.", 401
            )

        session["user_id"] = user[0]

        cursor.close()
        connection.close()

        return redirect("/")

    else:
        return render_template("login.html")
