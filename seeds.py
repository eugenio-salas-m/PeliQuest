from db import db
from app import app
from models import User, Message
from flask_bcrypt import Bcrypt

with app.app_context():
    db.create_all()
    