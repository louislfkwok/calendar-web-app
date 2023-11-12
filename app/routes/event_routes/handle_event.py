from app import app
from app.helpers import apology, login_required
from app.utils.bound_generators import get_bound, get_left_bound, get_right_bound
from app.utils.validators import check_end_time, check_start_time, check_weekday
from flask import redirect, request, session

import sqlite3

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
