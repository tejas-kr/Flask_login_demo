from flask import Flask, Blueprint
from decouple import config

from .custom_logger import get_logger


def create_app(config_filename='setting.py'):

    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    # SETTING LOGGER
    fileHandler, streamHandler = get_logger()

    app.logger.addHandler(fileHandler)
    app.logger.addHandler(streamHandler)

    from .show_data import show_data
    from .authentication import authentication
    app.register_blueprint(show_data)
    app.register_blueprint(authentication)

    return app
