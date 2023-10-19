import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import secrets
from flask import Flask, request, render_template, redirect, url_for, session, Blueprint
from models import *
from flask_migrate import Migrate
from routes.admin import admin_page
from routes.user import user_page

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/perpustakaan'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)

db.init_app(app)
migrate = Migrate(app, db)

@app.errorhandler(404)
def page_not_found(error):
    return "404 Page Not Found", 404


app.register_blueprint(admin_page)
app.register_blueprint(user_page)

import base64
def base64_encode(data):
    return base64.b64encode(data).decode('utf-8')

from jinja2 import Environment
# Add the custom filter to the Jinja2 environment
app.jinja_env.filters['b64encode'] = base64_encode