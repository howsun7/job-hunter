from flask import Flask
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from . import commands
from .config import Config
from .models import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)


app.cli.add_command(commands.print_data)
app.cli.add_command(commands.seed_db)
app.cli.add_command(commands.table_cleanup)

# avoid import error for partially initialized modules
from app.routes import api
app.register_blueprint(api.bp)