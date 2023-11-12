from flask import Blueprint, redirect, request, session
from helpers import login_required

import sqlite3

delete_task_bp = Blueprint('delete_task', __name__)


@delete_task_bp.route("/delete-task", methods=["POST"])
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
