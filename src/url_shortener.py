import contextlib
import os
import sqlite3

from flask import Flask

import config


app = Flask(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    if not os.path.exists(app.config['DATABASE']):
        with contextlib.closing(connect_db()) as db:
            # should schema.sql path be used here or defined at the top of
            # the file?
            with app.open_resource('../db/schema.sql') as schema:
                contents = schema.read()
                db.executescript(contents)


@app.route('/')
def show_mainpage():
    return app.config['DATABASE']
    
            
def main():
    # TODO:
    # check for DB's existence and if it doesn't exist, initialize it
    # using schema.sql; part this out into its own fn obviously.
    app.config.from_object(config)
    init_db()
    app.run()


if __name__ == '__main__':
    main()
