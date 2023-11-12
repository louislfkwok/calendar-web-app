from flask import Blueprint, redirect, request, session
from helpers import apology, login_required

import sqlite3

edit_task_bp = Blueprint('edit_task', __name__)


@edit_task_bp.route("/edit-task", methods=["POST"])
@login_required
def edit_task():
    connection = sqlite3.connect("calendar.db")
    cursor = connection.cursor()

    user_id = session["user_id"]

    id = request.form.get("id")
    name = request.form.get("name")

    if not name:
        return apology("task name required. please enter a name for your task.")

    cursor.execute(
        "UPDATE tasks SET name = ? WHERE id = ? AND user_id = ?",
        (
            name,
            id,
            user_id,
        ),
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/")
