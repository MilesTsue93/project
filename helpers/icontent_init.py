"""
Refactored from a tutorial by Abdelhadi Dyouri on digitalocean.com on November 17, 2021.
url: https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
to read the sql script to create a database. Meant to run one time only.
"""
import sqlite3

connection = sqlite3.connect('icontent.db')

with open('db/schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()