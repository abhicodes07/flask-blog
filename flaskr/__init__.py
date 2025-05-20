import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the application
    # instance_relative_config tells the app that configuration will be stored in instance folder
    # The instance folder is designed to not be under version control and be deployment specific.
    app = Flask(__name__, instance_relative_config=True)

    # app default configuration
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, world!"

    from . import db

    db.init_app(app)

    return app
