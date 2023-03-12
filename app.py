import sqlite3 
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from string import Template
#import requests

import os
import datetime

from helpers.helper import login_required, read_config
from googleapiclient.discovery import build

# directory for application - 
# to be concatenated with database relative path
current_directory = os.path.dirname(os.path.abspath(__file__))

# HTML template to dynamically embed youtube videos on content page
# code borrowed from this tutorial: 
# http://www.compjour.org/lessons/flask-single-page/simple-youtube-viewing-flask-app/
HTML_TEMPLATE = Template("""
      <h2>
        YouTube video link: 
        <a href="https://www.youtube.com/watch?v=${youtube_id}?autoplay=1">
          ${youtube_id}
        </a>
      </h2>
    
      <iframe src="https://www.youtube.com/embed/${youtube_id}" width="853" height="480" frameborder="0" allowfullscreen></iframe>""")

# Configure application
app = Flask(__name__)
config = read_config()
API_KEY = config["FTPSettings"]["api_key"]

# for youtube api calls
api_service_name = "youtube"
api_version = "v3"
youtube = build(api_service_name, api_version, developerKey=API_KEY)  


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
    
    # variable to use for current logged-in user
    user = session["user_id"]

    # defining connection instance
    # to get the sqlite db connection
    conn = sqlite3.connect(current_directory + '/icontent.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor() 
    
    history = cursor.execute("SELECT video_name, text_content, time_logged FROM history WHERE user_id = '" + user + "'").fetchall()
    print(history)
    print()

    # commit the change in db
    conn.commit()

    # close cursor
    cursor.close()

    # return the html page to show user content history
    return render_template('index.html', history=history)


@app.route("/about")
@login_required
def about():
    return render_template("about.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # defining connection instance
    # to get the sqlite db connection
    conn = sqlite3.connect(current_directory + '/icontent.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

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
        rows = cursor.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()
        
        print(check_password_hash(request.form.get("username"), request.form.get("password")))
        # Ensure username exists and password is correct
        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("error.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["username"]

        # commit the change in db
        conn.commit()

        # close the cursor
        cursor.close()

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        cursor.close()
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
    
    # variable to use for current logged-in user
    user = session["user_id"]

    # defining connection instance
    # to get the sqlite db connection
    conn = sqlite3.connect(current_directory + '/icontent.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # to disable OAuth authentication (???)
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    if request.method == "POST":
        
        # for youtube api calls
        api_service_name = "youtube"
        api_version = "v3"
        youtube = build(
            api_service_name, api_version, developerKey=API_KEY)  
        
        # store query in variable to use for parsed JSON results from API
        video = request.form.get("search")

        request_api = youtube.search().list( 
            part="snippet",
            q=video,
            type="video"
        )

        response = request_api.execute()
        print(response)

        # TODO will parse JSON to determine what to access
        
        video_name = response["items"][0]["id"]["videoId"]
        video_title = response["items"][0]["snippet"]["title"]

        # will use this variable for text to display on index page
        # as well as content page
        entry = request.form.get("entry")

        # for time_logged
        time_logged = datetime.datetime.now()

        # Insert data into history table
        cursor.execute("INSERT INTO history (video_name, text_content, time_logged, user_id) VALUES (?, ?, ?, ?)", (video_title, entry, time_logged, user)).fetchall()
        
        # committing change and closing cursor
        conn.commit()

        cursor.close()
        
        # post will redirect user to index page
        # to see the content they generated thus far
        return render_template("content.html", video_name=video_name)
    
    else:
        cursor.close()
        return render_template("content.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    print(current_directory + "/icontent.db")
    print()
    # defining connection instance
    # to get the sqlite db connection
    conn = sqlite3.connect(current_directory + '/icontent.db')
    cursor = conn.cursor() 
    cursor.row_factory = lambda cursor, row: row[0]

    #user = session["user_name"]
    # if user needs page displayed only
    if request.method == "GET":
        return render_template("register.html")

    # if user is submitting data to form fields on register page
    if request.method == "POST":

        # for validating against existing data in users table
        usernames = cursor.execute("SELECT username FROM users").fetchall()

        # if user doesn't fill every required form field,
        # return error function
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if (username in usernames):
            return render_template("error.html")
        elif not username or not password or not confirmation:
            return render_template("error.html")
        elif (password != confirmation):
            return render_template("error.html")
        else:
            # if all checks out, register the new user using a hashed password :)
            # generate hash for password to encrypt
            hashed_password = generate_password_hash(password)
            new_id_db = cursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hashed_password))
            session["user_id"] = new_id_db.fetchone()
                 
            # commit change to db
            conn.commit()
            # close cursor
            cursor.close()
            
            # return login tmeplate
            return render_template("content.html")

if __name__ == "__main__":
    app.run(debug=True)
