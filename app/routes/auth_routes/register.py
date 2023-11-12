from app import app
from app.helpers import apology
from flask import redirect, render_template, request
from werkzeug.security import generate_password_hash

import sqlite3

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        connection = sqlite3.connect("calendar.db")
        cursor = connection.cursor()

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("username required. please enter a username.")

        if not password:
            return apology("password required. please enter a password.")

        if not confirmation:
            return apology(
                "password confirmation required. please enter a confirmation password."
            )

        if password != confirmation:
            return apology("passwords do not match. please ensure they are the same.")

        users_with_same_username = cursor.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchall()

        if len(users_with_same_username) != 0:
            return apology(
                "username already in use. please enter a different username.", 409
            )

        hash = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/login")

    else:
        return render_template("register.html")
