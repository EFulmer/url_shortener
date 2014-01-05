from contextlib import closing
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
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_mainpage():
    init_db()
    cur = g.db.execute('SELECT * FROM Link;')
    return repr(cur)


def main():
    app.config.from_object(config)
    if not os.path.exists(app.config['DATABASE']):
        init_db()
    app.run()


if __name__ == '__main__':
    main()
