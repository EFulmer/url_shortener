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
import tlds


app = Flask(__name__)


def connect_db():
    """Return a connection to the app's (SQLite3) database."""
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    """Initialize a new database."""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    """
    Open a connection to the database, before actually handling the 
    request.
    """
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    """
    Close the connection to the database after the request is handled.
    """
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_mainpage():
    """Show the main page."""
    return render_template('shorten_url.html')


@app.route('/add', methods=['POST'])
def add_url():
    """
    Insert the submitted URL into the database with a short version. 
    Then redirect the user back to the main page, with a flashed 
    message containing the shortened URL.
    """
    url = request.form['url']

    if not tlds.has_valid_tld(url):
        flash("Sorry, but {0} isn't a valid URL. ".format(url))
        return redirect(url_for('show_mainpage'))

    try:
        cr = g.db.cursor()
        cr.execute('INSERT INTO Link (longurl) VALUES (?);',
                [request.form['url']])
        cr.execute('INSERT INTO Redirect (longurl, count) VALUES (?, 0);',
                [request.form['url']])
        res = cr.execute('SELECT id FROM Link WHERE longurl = (?);',
                [request.form['url']])

        short_url = res.fetchone()[0]
        g.db.commit()
        cr.close()
    except Exception:
        # TODO log error msg and send to me.
        flash("We're sorry, but an error occurred.")
    else:
        flash('Short url is {0}/{1}'.format(app.config['HOSTNAME'], 
                                            short_url))
    
    return redirect(url_for('show_mainpage'))


@app.route('/<int:short_url>', methods=['GET'])
def reroute_url(short_url):
    """Redirect the shortened URL to its actual destination."""
    cr = g.db.execute('''SELECT L.longurl, R.count 
                         FROM Link L 
                         LEFT JOIN Redirect R WHERE id = (?)''',
            [short_url])
    res = cr.fetchone()
    cr.close()

    # None returned if no results from query; 
    if not res:
        flash("Sorry, but there's no URL with the shortened form {0}.".format(
            short_url))
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
    """Set up a new database for the URL shortener and then run it."""
    app.config.from_object(config)
    if not os.path.exists(app.config['DATABASE']):
        init_db()
    if not os.path.exists(tlds.TLD_FILE):
       tlds.write_tlds_to_file()
    app.run()


if __name__ == '__main__':
    main()
