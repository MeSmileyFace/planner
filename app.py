from typing import List
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
from sqlalchemy.sql.expression import desc, select
from sqlparse.sql import If
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp
from datetime import datetime, date, timedelta

import json

from helpers import login_required, apology, striptime
from flask_cors import CORS


app = Flask(__name__)


@app.template_filter('strftime')
def format_datetime(date: datetime) -> str:
    return date.strftime('%d-%m-%Y')


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///planner.db")


@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    rows = db.execute(
        "SELECT id, name, description, selected_date AS chosenDate, due_date as dueDate, finished, date_finished AS datefinished FROM tasks WHERE user_id=? ORDER BY due_date", user_id)
    list4jinja = []
    today = datetime.today().date()
    for row in rows:
        obj = {}
        obj = row
        obj["startDate"] = striptime(row["chosenDate"]).date()
        obj["endDate"] = striptime(row["dueDate"]).date()
        x = (today-obj["startDate"]).days
        progressDays = 1 if x == 0 else x
        y = (obj["endDate"]-obj["startDate"]).days
        totalDays = 1 if y == 0 else y
        obj["percentage"] = round((progressDays*100)/totalDays)
        list4jinja.append(obj)
    finishedTasks = filter(lambda x: (x["finished"]), list4jinja)
    activeTasks = filter(lambda x: (
        x["startDate"] <= today and today <= x["endDate"] and not x["finished"]), list4jinja)
    overdueTasks = filter(lambda x: (
        x["endDate"] < today and not x["finished"]), list4jinja)
    upcomingTasks = filter(lambda x: (
        today < x["startDate"] and not x["finished"]), list4jinja)
    activeTasks4jinja=sorted(list(activeTasks),key=lambda x: x["percentage"], reverse=True)
    
    
    return render_template("index.html", activeTasks=activeTasks4jinja, overdueTasks=overdueTasks, upcomingTasks=upcomingTasks, finishedTasks=finishedTasks)


@app.route("/calendar")
@login_required
def calendar():
    user_id = session["user_id"]
    rows = db.execute("SELECT username FROM users WHERE id=?", user_id)
    username = rows[0]["username"]
    return render_template("calendar.html", username=username)


@app.route("/ftasks")
@login_required
def finished():
    finishedTasks = {}
    user_id = session["user_id"]
    rows = db.execute("""
        SELECT name, description, selected_date AS chosenDate,
        due_date as dueDate, finished, date_finished AS datefinished
        FROM tasks 
        WHERE user_id=?""", user_id)
    finishedTasks = filter(lambda x: (x["finished"]), rows)
    finished4jinja = map(lambda x: {
        "name": x["name"],
        "description": x["description"],
        "startDate": striptime(x["chosenDate"]),
        "endDate": striptime(x["dueDate"]),
        "finishDate": striptime(x["datefinished"]),
        "daysUntilEnd": (striptime(x["dueDate"])-striptime(x["datefinished"])).days
    }, finishedTasks)
    return render_template("ftasks.html", finishedTasks=finished4jinja)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        # Ensure confirmation was submitted
        elif not confirmation:
            return apology("must provide confirmation", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          username)

        # Ensure confirmation matches password
        if confirmation != password:
            return apology("Confirmation does not match password", 403)

        # Ensure username doesn't already exist
        if len(rows) != 0:
            return apology("Username already exists", 403)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                       username, generate_password_hash(password))

            # Redirect user to home page
            return redirect("/login")
        except Exception as e:
            print(e)
            return apology("Registration failed", 500)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    # clear session user
    session.clear()

    # user reached route via POST method
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Missing username
        if not username:
            return apology("username missing", 403)

        # Missing password
        if not password:
            return apology("password missing", 403)

        rows = db.execute("SELECT * FROM users WHERE username=?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        return redirect("/")
    else:
        return render_template("login.html")


@ app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/dateEvent", methods=["GET", "POST"])
def dateEvent():
    chosenYear = int(request.form.get("chosenYear"))
    chosenMonth = int(request.form.get("chosenMonth"))
    chosenDate = int(request.form.get("chosenDate"))
    constructedDate = datetime(
        year=chosenYear, month=chosenMonth, day=chosenDate)
    return render_template("dateEvent.html", constructedDate=constructedDate)


@app.route("/learnAjax", methods=["POST"])
def saveEvent():
    b = request.get_json()
    print(b)
    res = {
        "my": "new",
        "level_of": "fed_up"
    }
    return json.dumps(res)


@app.route("/dateEventAjax", methods=["POST"])
def dateEventAjax():
    r = request.get_json()
    chosenDate = striptime(r["chosenDate"])
    user_id = session["user_id"]
    rows = db.execute(
        "SELECT * FROM tasks WHERE user_id=? AND DATE(selected_date)=DATE(?) AND finished=0", user_id, chosenDate)
    return json.dumps(rows)


@app.route("/deleteEventAjax", methods=["POST"])
def deleteEventAjax():
    req = request.get_json()
    task_id = req["taskId"]
    user_id = session["user_id"]
    rows = db.execute("SELECT user_id FROM tasks WHERE id=?", task_id)
    if (user_id != rows[0]["user_id"]):
        return apology("This task does not belong to you", 403)
    db.execute(
        "UPDATE tasks SET finished=1, date_finished=DATE('now') WHERE id=?", task_id)
    res = {
        "taskId": task_id
    }

    return json.dumps(res)


@app.route("/saveTask", methods=["POST"])
def saveTask():
    name = request.form.get("name")
    description = request.form.get("description")
    dueDate = striptime(request.form.get("dueDate"))
    selectedDate = striptime(request.form.get("selectedDate"))
    user_id = session["user_id"]
    db.execute("INSERT INTO tasks (name, description, due_date, selected_date, finished, user_id) VALUES(?, ?, DATE(?),DATE(?), 0, ?)",
               name, description, dueDate, selectedDate, user_id)

    return redirect("/calendar")
