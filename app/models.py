# Add any model classes for Flask-SQLAlchemy here

from . import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    photo = db.Column(db.String)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    profile = db.relationship('Profile', backref='user', uselist=False, cascade="all, delete")
    favourites = db.relationship('Favourite', foreign_keys='Favourite.user_id_fk', backref='user', cascade="all, delete")
    favourited_by = db.relationship('Favourite', foreign_keys='Favourite.fav_user_id_fk', backref='fav_user', cascade="all, delete")


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String)
    parish = db.Column(db.String)
    biography = db.Column(db.String)
    sex = db.Column(db.String)
    race = db.Column(db.String)
    birth_year = db.Column(db.Integer)
    height = db.Column(db.Float)
    fav_cuisine = db.Column(db.String)
    fav_colour = db.Column(db.String)
    fav_school_subject = db.Column(db.String)  # Fixed typo from "fav_school_sibject"
    political = db.Column(db.Boolean)
    religious = db.Column(db.Boolean)
    family_oriented = db.Column(db.Boolean)


class Favourite(db.Model):
    __tablename__ = 'favourite'

    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fav_user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)