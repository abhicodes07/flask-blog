import sqlite3
from datetime import datetime

import click
from flask import current_app, g


def get_db():
    # g object is unique for every request.
    # used for storing data accessed by mulitple functions
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],  # points to the flask application
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row  # returns rows that behave like dicts

    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# initialize the scheme for database
def init_db():
    db = get_db()

    # open_resource opens a file relative to flaskr package
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


# define custom command line command init-db that invokes
# init_db() function and shows a successful message
@click.command("init-db")
def init_db_command():
    """clear the exisiting data in database and create new table"""
    init_db()
    click.echo("Initialized the database.")


# specify how to interpret timestamp values in the database
sqlite3.register_converter("timestamp", lambda v: datetime.fromisoformat(v.decode()))


# register with the application
def init_app(app):
    app.teardown_appcontext(
        close_db
    )  # call that function when cleaning up after returning the response
    app.cli.add_command(
        init_db_command
    )  # add new command which can be callded using flask
