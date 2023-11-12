from app import app
from app.helpers import login_required
from flask import redirect, request, session

import sqlite3

@app.route("/delete-task", methods=["POST"])
@login_required
def delete_task():
    connection = sqlite3.connect("calendar.db")
    cursor = connection.cursor()

    user_id = session["user_id"]

    id = request.form.get("id")

    cursor.execute(
        "DELETE FROM tasks WHERE id = ? AND user_id = ?",
        (
            id,
            user_id,
        ),
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/")
