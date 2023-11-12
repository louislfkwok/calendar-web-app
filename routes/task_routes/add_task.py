from flask import Blueprint, redirect, request, session
from helpers import apology, login_required

import sqlite3

add_task_bp = Blueprint('add_task', __name__)


@add_task_bp.route("/add-task", methods=["POST"])
@login_required
def add_task():
    connection = sqlite3.connect("calendar.db")
    cursor = connection.cursor()

    user_id = session["user_id"]

    name = request.form.get("name")
    priority = request.form.get("priority")
    estimate = request.form.get("estimate")
    deadline = request.form.get("deadline")

    if not name:
        return apology("task name required. please enter a name for your task.")

    cursor.execute(
        "INSERT INTO tasks (name, priority, estimate, deadline, user_id) VALUES (?, ?, ?, ?, ?)",
        (
            name,
            priority,
            estimate,
            deadline,
            user_id,
        ),
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/")
