from app import app
from app.config.constants import WEEKDAYS
from app.helpers import login_required
from app.utils.bound_generators import get_bound, get_left_bound, get_right_bound
from flask import redirect, session

import sqlite3

@app.route("/allocate-tasks", methods=["POST"])
@login_required
def allocate_tasks():
    connection = sqlite3.connect("calendar.db")
    cursor = connection.cursor()

    user_id = session["user_id"]

    cursor.execute(
        "SELECT * FROM tasks WHERE user_id = ?",
        (
            user_id,
        ),
    )

    tasks = cursor.fetchall()

    sorted_tasks = sorted(tasks, key = lambda x : (x[4], x[2]))

    for task in sorted_tasks:
        current_weekday = "WED" # TODO: Current weekday
        current_start_time = "09:00" # TODO: User-defined start of day
        event_created = False

        while event_created == False:
            duration = task[3]
            current_end_hour = int(current_start_time[:2]) + duration

            if current_end_hour > 21: # TODO: User-defined end of day
                new_weekday_index = (WEEKDAYS.index(current_weekday) + 1) % 7
                current_weekday = WEEKDAYS[new_weekday_index]
                current_start_time = "07:00"
                continue
            
            current_end_time = ('0' if current_end_hour < 10 else '') + str(current_end_hour) + ":00"

            left_bound = get_left_bound(current_weekday)
            right_bound = get_right_bound(current_weekday)
            top_bound = get_bound(current_start_time)
            bottom_bound = get_bound(current_end_time)

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
            
            if slot_occupied:
                new_start_hour = int(current_start_time[:2]) + 1
                current_start_time = ('0' if new_start_hour < 10 else '') + str(new_start_hour) + ":00"
                continue

            name = task[1]

            cursor.execute(
                "INSERT INTO events (name, weekday, start_time, end_time, user_id) VALUES (?, ?, ?, ?, ?)",
                (
                    name,
                    current_weekday,
                    current_start_time,
                    current_end_time,
                    user_id,
                ),
            )

            id = cursor.execute(
                "SELECT id FROM events WHERE name = ? AND weekday = ? AND start_time = ? AND end_time = ? AND user_id = ?",
                (
                    name,
                    current_weekday,
                    current_start_time,
                    current_end_time,
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

            event_created = True

    for task in tasks:
        cursor.execute("DELETE FROM tasks WHERE id = ?",
            (
                task[0],
            ),
        )
    
    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/")
