from config.constants import WEEKDAYS
from helpers import login_required
from flask import Blueprint, render_template, session

import sqlite3

index_bp = Blueprint('index', __name__)


@index_bp.route("/")
@login_required
def index():
    connection = sqlite3.connect("calendar.db")
    cursor = connection.cursor()

    user_id = session["user_id"]

    tasks = cursor.execute(
        "SELECT * FROM tasks WHERE user_id = ?", (user_id,)
    ).fetchall()

    events = cursor.execute(
        "SELECT * FROM events JOIN event_styles ON events.id = event_styles.event_id WHERE events.user_id = ?",
        (user_id,),
    ).fetchall()

    boxes_used_dict = cursor.execute(
        "SELECT box_used FROM boxes_used WHERE boxes_used.user_id = ?",
        (user_id,),
    ).fetchall()

    boxes_used_list = list()

    for box_used in boxes_used_dict:
        boxes_used_list.append(box_used[0])

    cursor.close()
    connection.close()

    return render_template(
        "index.html",
        weekdays=WEEKDAYS,
        tasks=tasks,
        events=events,
        boxes_used=boxes_used_list,
    )
