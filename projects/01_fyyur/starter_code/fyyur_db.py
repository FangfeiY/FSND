from flask_moment import Moment
from flask_migrate import Migrate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database:
# postgresql://postgres:postgres@localhost:5432/fyyur
migrate = Migrate(app, db)