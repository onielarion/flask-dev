from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Create a table for the note

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date= db.Column(db.DateTime(timezone=True), default=func.now())
    # Create a relationship between the note and the user table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Create a table for the user

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True) # Email must be unique
    password = db.Column(db.String(150), nullable=False)
    firstname = db.Column(db.String(150), nullable=False)
    lastname = db.Column(db.String(150), nullable=False)
    # Create a relationship between the user and the note table
    notes = db.relationship('Note', backref='user', passive_deletes=True)

