-- possible future improvement: switch from sqlite3 to postgres or mysql?
-- those may be a little "heavy" for what will probably never amount to 
-- more than a toy web app

DROP TABLE IF EXISTS Links;

CREATE TABLE Links (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	url TEXT NOT NULL
);
