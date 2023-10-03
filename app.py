from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

from helpers import apology, login_required

WEEKDAYS = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]

app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def check_weekday(weekday):
    return weekday in WEEKDAYS


def check_start_time(time):
    if len(time) != 5:
        return False

    if time[2] != ':':
        return False

    hour, minute = time.split(':')

    if minute != "00":
        return False

    hour_found = False
    for hour_int in range(24):
        hour_str = str(hour_int)
        if len(hour_str) == 1:
            hour_str = "0" + hour_str

        if hour == hour_str:
            hour_found = True
            break

    if not hour_found:
        return False

    return True


def check_end_time(time):
    if len(time) != 5:
        return False

    if time[2] != ':':
        return False

    hour, minute = time.split(':')

    if minute != "00":
        return False

    hour_found = False
    for hour_int in range(1, 25):
        hour_str = str(hour_int)
        if len(hour_str) == 1:
            hour_str = "0" + hour_str

        if hour == hour_str:
            hour_found = True
            break

    if not hour_found:
        return False

    return True


def get_left_bound(weekday):
    cnt = 1
    for WEEKDAY in WEEKDAYS:
        if weekday == WEEKDAY:
            return cnt
        cnt += 1


def get_right_bound(weekday):
    cnt = 2
    for WEEKDAY in WEEKDAYS:
        if weekday == WEEKDAY:
            return cnt
        cnt += 1


def get_bound(time):
    hour_part = time.split(":")[0]
    hour = int(hour_part)
    return hour + 1


@app.route("/")
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


@app.route("/add-task", methods=["POST"])
@login_required
def add_task():
    connection = sqlite3.connect("calendar.db")
    cursor = connection.cursor()

    user_id = session["user_id"]

    name = request.form.get("name")

    if not name:
        return apology("task name required. please enter a name for your task.")

    cursor.execute(
        "INSERT INTO tasks (name, user_id) VALUES (?, ?)",
        (
            name,
            user_id,
        ),
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/")


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


@app.route("/edit-task", methods=["POST"])
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


@app.route("/handle-event", methods=["POST"])
@login_required
def handle_event():
    connection = sqlite3.connect("calendar.db")
    cursor = connection.cursor()

    user_id = session["user_id"]

    if "add_event" in request.form:
        name = request.form.get("name")
        weekday = request.form.get("weekday")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")

        if not name:
            return apology("event name required. please enter a name for your event.")

        if not weekday:
            return apology(
                "day of the week required. please select a day for your event."
            )

        if not check_weekday(weekday):
            return apology(
                "invalid day of the week. please select a day for your event.", 422
            )

        if not start_time:
            return apology(
                "start time required. please select a start time for your event."
            )

        if not check_start_time(start_time):
            return apology(
                "invalid start time. please select a start time for your event.", 422
            )

        if not end_time:
            return apology(
                "end time required. please select an end time for your event."
            )

        if not check_end_time(end_time):
            return apology(
                "invalid end time. please select an end time for your event.", 422
            )

        if start_time >= end_time:
            return apology(
                "invalid time range. start time cannot be after end time.", 422
            )

        left_bound = get_left_bound(weekday)
        right_bound = get_right_bound(weekday)
        top_bound = get_bound(start_time)
        bottom_bound = get_bound(end_time)

        slot_occupied = False
        boxes_to_be_used = list()

        for column in range(left_bound, right_bound):
            for row in range(top_bound, bottom_bound):
                box_to_be_used = (column - 1) * 24 + row
                box_is_used = cursor.execute(
                    "SELECT COUNT(*) FROM boxes_used WHERE box_used = ? AND user_id = ?",
                    (
                        box_to_be_used,
                        user_id,
                    ),
                ).fetchall()

                if box_is_used[0][0] > 0:
                    slot_occupied = True
                    break
                else:
                    boxes_to_be_used.append(box_to_be_used)

        if not slot_occupied:
            cursor.execute(
                "INSERT INTO events (name, weekday, start_time, end_time, user_id) VALUES (?, ?, ?, ?, ?)",
                (
                    name,
                    weekday,
                    start_time,
                    end_time,
                    user_id,
                ),
            )

            id = cursor.execute(
                "SELECT id FROM events WHERE name = ? AND weekday = ? AND start_time = ? AND end_time = ? AND user_id = ?",
                (
                    name,
                    weekday,
                    start_time,
                    end_time,
                    user_id,
                ),
            ).fetchall()[0][0]
            cursor.execute(
                "INSERT INTO event_styles (event_id, column_start, column_end, row_start, row_end) VALUES (?, ?, ?, ?, ?)",
                (
                    id,
                    left_bound,
                    right_bound,
                    top_bound,
                    bottom_bound,
                ),
            )

            for box_to_be_used in boxes_to_be_used:
                cursor.execute(
                    "INSERT INTO boxes_used (event_id, box_used, user_id) VALUES (?, ?, ?)",
                    (
                        id,
                        box_to_be_used,
                        user_id,
                    ),
                )

            connection.commit()

        else:
            return apology(
                "time slot conflict. specified time range already has an event.", 409
            )

    elif "edit_event" in request.form:
        id = request.form.get("id")
        name = request.form.get("name")
        weekday = request.form.get("weekday")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")

        if not name:
            return apology("event name required. please enter a name for your event.")

        if not weekday:
            return apology(
                "day of the week required. please select a day for your event."
            )

        if not check_weekday(weekday):
            return apology(
                "invalid day of the week. please select a day for your event.", 422
            )

        if not start_time:
            return apology(
                "start time required. please select a start time for your event."
            )

        if not check_start_time(start_time):
            return apology(
                "invalid start time. please select a start time for your event.", 422
            )

        if not end_time:
            return apology(
                "end time required. please select an end time for your event."
            )

        if not check_end_time(end_time):
            return apology(
                "invalid end time. please select an end time for your event.", 422
            )

        if start_time >= end_time:
            return apology(
                "invalid time range. start time cannot be after end time.", 422
            )

        left_bound = get_left_bound(weekday)
        right_bound = get_right_bound(weekday)
        top_bound = get_bound(start_time)
        bottom_bound = get_bound(end_time)

        slot_occupied = False
        boxes_to_be_used = list()

        for column in range(left_bound, right_bound):
            for row in range(top_bound, bottom_bound):
                box_to_be_used = (column - 1) * 24 + row
                box_is_used = cursor.execute(
                    "SELECT COUNT(*) FROM boxes_used WHERE event_id != ? AND box_used = ? AND user_id = ?",
                    (
                        id,
                        box_to_be_used,
                        user_id,
                    ),
                ).fetchall()

                if box_is_used[0][0] > 0:
                    slot_occupied = True
                    break
                else:
                    boxes_to_be_used.append(box_to_be_used)

        if not slot_occupied:
            cursor.execute(
                "UPDATE events SET name = ?, weekday = ?, start_time = ?, end_time = ? WHERE id = ? AND user_id = ?",
                (
                    name,
                    weekday,
                    start_time,
                    end_time,
                    id,
                    user_id,
                ),
            )

            cursor.execute(
                "UPDATE event_styles SET column_start = ?, column_end = ?, row_start = ?, row_end = ? WHERE event_id = ?",
                (
                    left_bound,
                    right_bound,
                    top_bound,
                    bottom_bound,
                    id,
                ),
            )

            cursor.execute(
                "DELETE FROM boxes_used WHERE event_id = ? AND user_id = ?",
                (
                    id,
                    user_id,
                ),
            )
            for box_to_be_used in boxes_to_be_used:
                cursor.execute(
                    "INSERT INTO boxes_used (event_id, box_used, user_id) VALUES (?, ?, ?)",
                    (
                        id,
                        box_to_be_used,
                        user_id,
                    ),
                )

            connection.commit()

        else:
            return apology(
                "time slot conflict. specified time range already has an event.", 409
            )

    elif "delete_event" in request.form:
        id = request.form.get("id")

        cursor.execute("DELETE FROM event_styles WHERE event_id = ?", (id,))

        cursor.execute(
            "DELETE FROM boxes_used WHERE event_id = ? AND user_id = ?",
            (
                id,
                user_id,
            ),
        )

        cursor.execute("DELETE FROM events WHERE id = ? AND user_id = ?", (id, user_id))

        connection.commit()

    cursor.close()
    connection.close()

    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
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


@app.route("/logout")
def logout():
    session.clear()

    return redirect("/login")


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
