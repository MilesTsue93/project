"""
Refactored from a tutorial by Abdelhadi Dyouri on digitalocean.com on November 17, 2021.
url: https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
"""

import sqlite3

connection = sqlite3.connect('icontent.db')


with open('db/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

connection.commit()
connection.close()