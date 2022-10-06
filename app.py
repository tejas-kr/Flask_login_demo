from flask import Flask, Blueprint
# from flask_login import LoginManager
import logging

from show_data import show_data
from authentication import authentication

app = Flask(__name__)
app.secret_key = b'd177d7d81402930afec6d60b960426b87ccd0727b11942a515239ec9a09fac34'

# Logging setup
logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
formatter = logging.Formatter(logFormatStr,'%m-%d %H:%M:%S')

fileHandler = logging.FileHandler("logs/summary.log")
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)

streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(formatter)

app.logger.addHandler(fileHandler)
app.logger.addHandler(streamHandler)


# login_manager = LoginManager()
# login_manager.init_app(app)

app.register_blueprint(show_data)
app.register_blueprint(authentication)

@app.route('/')
def index():
    return "<h3><i>Welcome to login demo app</i></h3>"