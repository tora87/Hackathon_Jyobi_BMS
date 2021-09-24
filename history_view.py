from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
from databases.history_db import select_history

hist = Blueprint('rental_history', __name__, url_prefix='/rental_history')


@hist.route('/')
def history_page():
    if "user_id" not in session:
        return redirect("/")
    if session["user_id"][0] == "0":
        session["history"] = select_history()
    else:
        session["history"] = select_history(id=session["user_id"])
    return render_template('history.html')