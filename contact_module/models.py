from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from extensions import db


class ContactUS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(300), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_read_by_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<ContactUS {self.title}>"


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), nullable=True)
