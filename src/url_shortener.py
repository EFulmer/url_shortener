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
    return render_template('shorten_url.html')

@app.route('/add', methods=['POST'])
def add_url():
    # add the thing to the db
    # TODO: flash message with shortened URL
    # or build a new page with it.
    # better idea - page with all URLS given and their shortened
    # versions.
    cr = g.db.cursor()
    # TODO: check that URL is valid?
    cr.execute('INSERT INTO Link (url) VALUES (?);',
            [request.form['url']])
    g.db.commit()
    cr.close()
    return render_template('shorten_url.html')


def main():
    app.config.from_object(config)
    # FIXME only init_db iff app.cfg doesn't exist
    # using if not os.path.exists(app.config['DATABASE'] fails for 
    # some reason
    init_db()
    app.run()


if __name__ == '__main__':
    main()
