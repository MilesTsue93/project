DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS sqlite_sequence(name, seq);


CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    hash TEXT NOT NULL,
    username TEXT NOT NULL
);

CREATE UNIQUE INDEX username ON users (username);
CREATE TABLE sqlite_sequence(name, seq);