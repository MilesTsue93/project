DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS history;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    hash TEXT NOT NULL,
    username TEXT NOT NULL
);

CREATE TABLE history (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    video_name TEXT,
    text_content TEXT,
    time_logged DATETIME NOT NULL default(current_timestamp),
    'user_id' INTEGER
);

CREATE TABLE """sqlite_sequence"""(name,seq);
CREATE UNIQUE INDEX username ON users (username);
