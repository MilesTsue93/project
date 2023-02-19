import configparser

from flask import redirect, render_template, request, session
from functools import wraps

# Method to read config file settings
# this code also taken from url: https://www.codeproject.com/Articles/5319621/Configuration-Files-in-Python
def read_config():
    config = configparser.ConfigParser()
    config.read('configurations.ini')
    return config


def error(message, code=400):
    """Render message as an error to user."""

    return render_template("error.html")

"""
This function was borrowed from CS50's last problem set 'Finance'. It is most useful
for logging in and out
"""
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

