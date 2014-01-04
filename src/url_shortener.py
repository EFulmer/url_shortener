import sqlite3

from flask import Flask

app = Flask(__name__)



def main():
    # TODO:
    # check for DB's existence and if it doesn't exist, initialize it
    # using schema.sql; part this out into its own fn obviously.
    app.run()


if __name__ == '__main__':
    main()
