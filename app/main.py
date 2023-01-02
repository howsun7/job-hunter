from flask import Flask
from flask_migrate import Migrate
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)


