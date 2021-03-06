from flask import Flask, render_template
from src.common.database import Database

__author__ = 'neil'


app = Flask(__name__)  # create the application instance
app.config.from_object('src.config')  # load config from file
app.secret_key = "123"


@app.before_first_request
def init_db():
    Database.initialise()


@app.route('/')
def home():
    return render_template('home.html')

from src.models.users.views import user_blueprint
from src.models.stores.views import store_blueprint
from src.models.alerts.views import alert_blueprint
app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(store_blueprint, url_prefix='/stores')
app.register_blueprint(alert_blueprint, url_prefix='/alerts')
