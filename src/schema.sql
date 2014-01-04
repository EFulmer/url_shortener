-- possible future improvement: switch from sqlite3 to postgres or mysql?
-- those may be a little "heavy" for what will probably never amount to 
-- more than a toy web app

DROP TABLE IF EXISTS Link;

CREATE TABLE Link (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    url TEXT NOT NULL
);
