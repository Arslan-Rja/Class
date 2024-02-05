from flask import Flask, session
from os import getenv
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "2683eb9ee0fd3b310df2b8b102a93518"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///arslanra"

db = SQLAlchemy(app)

import routes

