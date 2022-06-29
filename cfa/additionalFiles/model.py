from flask_sqlalchemy import UserMixin
from .. import db


class User(db.Model,UserMixin):
    """Your model here"""
    pass