from flask_sqlalchemy import UserMixin
from .. import db


class User(db,UserMixin):
    """Your model here"""
    pass