-- possible future improvement: switch from sqlite3 to postgres or mysql?
-- those may be a little "heavy" for what will probably never amount to 
-- more than a toy web app

DROP TABLE IF EXISTS Link;
DROP TABLE IF EXISTS Redirect;

CREATE TABLE Link (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    longurl TEXT NOT NULL
);

CREATE TABLE Redirect (
    longurl TEXT PRIMARY KEY,
    count INTEGER,
    FOREIGN KEY(longurl) REFERENCES Link(longurl)
);
    
