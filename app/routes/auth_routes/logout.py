from app import app
from flask import redirect, session

@app.route("/logout")
def logout():
    session.clear()

    return redirect("/login")
