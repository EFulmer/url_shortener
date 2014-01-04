import sqlite3

from flask import Flask

import config


app = Flask(__name__)


@app.route('/')
def show_mainpage():
    return 'hello world'

def main():
    # TODO:
    # check for DB's existence and if it doesn't exist, initialize it
    # using schema.sql; part this out into its own fn obviously.
    app.config.from_object(config)
    app.run()


if __name__ == '__main__':
    main()
