import sqlite3 
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

import json

from helpers.helper import error, login_required, read_config
from googleapiclient.discovery import build


# Configure application
app = Flask(__name__)
config = read_config()
API_KEY = config["FTPSettings"]["api_key"]

# for youtube api calls
api_service_name = "youtube"
api_version = "v3"
youtube = build(api_service_name, api_version, developerKey=API_KEY)

# to get the sqlite db connection

def get_db_connection():

    db = sqlite3.connect('icontent.db')
    db.row_factory = sqlite3.Row 
    return db    


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/')
@login_required
def index():
    
    user = session["user_id"]
    print(user)
    print()
    print()
    db = get_db_connection()
    history = db.execute('SELECT video_name, text_content, time_logged FROM history WHERE user_id = (SELECT username FROM users WHERE id = ?)', (user))

    db.close()
    return render_template('index.html', history=history)


@app.route("/about")
@login_required
def about():
    return render_template("about.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    db = get_db_connection()
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))

        # Ensure username exists and password is correct
        if not check_password_hash(rows.fetchall(), request.form.get("password")):
            return render_template("error.html")

        # Remember which user has logged in
        session["user_id"] = rows.fetchall()

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/content", methods=["GET", "POST"])
@login_required
def content():
    """Get video from YouTube API"""

    # call the api and use query to return results
    video = request.form.get("search")
    
    request = youtube.channels().list( 
        part="snippet",
        q=video,
        type="video"
    )

    response = request.execute()
    print()
    print()
    print(response)
    print()
    print()
    result = response[0]

    # TODO - use api to send a video on html page
    # based off of word searched for

    entry = request.form.get("entry")
    return render_template("content.html", result=result, entry=entry)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # defining connection instance
    db = get_db_connection()

    #user = session["user_name"]
    # if user needs page displayed only
    if request.method == "GET":
        return render_template("register.html")

    # if user is submitting data to form fields on register page
    if request.method == "POST":

        # for validating against existing data in users table
        username_data = db.execute("SELECT username FROM users")
        usernames = [user["username"] for user in username_data]

        # if user doesn't fill every required form field,
        # return error function
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if (username in usernames):
            return error("Username already exists.")
        elif not username or not password or not confirmation:
            return error("Please fill out all required fields.")
        elif (password != confirmation):
            return error("passwords do not match.")
        else:
            # if all checks out, register the new user using a hashed password :)
            # generate hash for password to encrypt
            hashed_password = generate_password_hash(password)
            new_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hashed_password))
    
            # Log new user in
            session["user_id"] = new_id.fetchall()
            
            return render_template("login.html")
