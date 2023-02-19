import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import error, login_required, lookup, read_config

# Configure application
app = Flask(__name__)
config = read_config()
API_KEY = config["FTPSettings"]['api_key']

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/about")
@login_required
def about():
    return render_template("about.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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
    response = request.get("https://www.googleapis.com/youtube/v3/")

    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

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
            return error("Username already exists.", 400)
        elif not username or not password or not confirmation:
            return error("Please fill out all required fields.", 400)
        elif (password != confirmation):
            return error("passwords do not match.", 400)
        else:
            # if all checks out, register the new user using a hashed password :)
            # generate hash for password to encrypt
            hashed_password = generate_password_hash(password)
            new_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)

            # Log new user in
            session["user_id"] = new_id
            return render_template("empty.html")



@app.route("/about", methods=["GET", "POST"])
@login_required
def about():
    """display info about what this web app does"""
    # TODO

    return redirect("/")