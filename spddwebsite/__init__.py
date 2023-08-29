from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dc521c243424f382543b5bd4aa769b98'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

spdd_db = SQLAlchemy()
spdd_db.init_app(app)
spdd_ma = Marshmallow()
spdd_ma.init_app(app)

from spddwebsite import routes