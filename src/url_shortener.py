import contextlib
import os
import sqlite3

from flask import Flask
from flask import request
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import render_template
from flask import flash

import config


app = Flask(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with contextlib.closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as schema:
            db.cursor().executescript(schema.read())
            db.cursor().execute('DROP TABLE IF EXISTS Link;')
            db.cursor().execute('''CREATE TABLE Link (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL
                    );''')
        db.commit()


def show_urls():
    connection = connect_db()
    result = connection.execute('SELECT * FROM Link;')
    return ''.join(r for r in result)


@app.route('/')
def show_mainpage():
    return show_urls()


def main():
    # TODO:
    # check for DB's existence and if it doesn't exist, initialize it
    # using schema.sql; part this out into its own fn obviously.
    app.config.from_object(config)
    init_db()
    app.run()


if __name__ == '__main__':
    main()
