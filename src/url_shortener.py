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
from flask import redirect

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
    cr.execute('INSERT INTO Link (longurl) VALUES (?);',
            [request.form['url']])
    cr.execute('INSERT INTO Redirect (longurl, count) VALUES (?, 0);',
            [request.form['url']])
    short_url = cr.execute('SELECT id FROM Link WHERE longurl = (?);',
            [request.form['url']])
    g.db.commit()
    cr.close()
    flash('Short url is {0}{1}'.format(url_for('show_mainpage'), short_url))
    # redirect to the main/top page ('/').
    return redirect(url_for('show_mainpage'))


@app.route('/<int:short_url>', methods=['GET'])
def reroute_url(short_url):
    # get longurl from short_url:
    cr = g.db.execute('''SELECT L.longurl, R.count 
                FROM Link L 
                LEFT JOIN Redirect R WHERE id = (?)''',
            [short_url])
    res = cr.fetchone()
    cr.close()

    # None returned if no results from query; 
    if not res:
        # TODO update main page to handle flashed messages.
        flash('Error: Unable to find site to redirect to.')
        return redirect(url_for('show_mainpage'))
    else:
        long_url, count = res
        g.db.execute('''UPDATE Redirect
                        SET longurl=(?), count=(?)
                        WHERE longurl=(?);''',
                        [long_url, count + 1, long_url])
        g.db.commit()
        return redirect(res[0])


def main():
    app.config.from_object(config)
    # FIXME only init_db iff app.cfg doesn't exist
    # using if not os.path.exists(app.config['DATABASE'] fails for 
    # some reason
    init_db()
    app.run()


if __name__ == '__main__':
    main()
