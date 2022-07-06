from flask import Flask
{% if "flask-sqlalchemy" in additional_plugin %}from flask_sqlalchemy import SQLAlchemy{% endif %}
{% if "flask-wtf" in additional_plugin %}from flask_wtf import CSRFprotect {% endif %}
{% if "flask-cors" in additional_plugin %}from flask_cors import CORS{% endif %}
{% if "flask-marshmallow" in additional_plugin %}from flask_marshmallow import Marshmallow {% endif %}
{% if "flask-debugtoolbar" in additional_plugin %}from flask_debugtoolbar import DebugToolbarExtension {% endif %}
{% if "flask-cache" in  additional_plugin %}from flask_caching import Cache {% endif %}
{% if "flask-compress" in additional_plugin %}from flask_compress import Compress {% endif %}
{% if auth == "flask-login" %}from flask_login import LoginManager{% endif %}
{% if auth == "flask-jwt-extended" %}from flask_jwt_extended import JWT{% endif %}

{% if "flask-sqlalchemy" in additional_plugin %}db = SQLAlchemy(session_options={"autoflush": False}){% endif %}
{% if "flask-wtf" in additional_plugin %}csrf = CSRFprotect() {% endif %}
{% if "flask-cors" in additional_plugin %}cors = CORS(){% endif %}
{% if "flask-marshmallow" in additional_plugin %}marshmallow = Marshmallow() {% endif %}
{% if "flask-debugtoolbar" in additional_plugin %}toolbar = DebugToolbarExtension() {% endif %}
{% if "flask-cache" in  additional_plugin %}cache = Cache(app) {% endif %}
{% if "flask-compress" in additional_plugin %}compress = Compress() {% endif %}

def create_app():
    app = Flask(__name__)
    {% if "flask-sqlalchemy" in additional_plugin %}db.init_app(app){% endif %}
    {% if "flask-wtf" in additional_plugin %}csrf.init_app(app){% endif %}
    {% if "flask-cors" in additional_plugin %}cors.init_app(app){% endif %}
    {% if "flask-marshmallow" in additional_plugin %}marshmallow.init_app(app){% endif %}
    {% if "flask-debugtoolbar" in additional_plugin %}toolbar.init_app(app){% endif %}
    {% if "flask-cache" in  additional_plugin %}cache.init_app(app){% endif %}
    {% if "flask-compress" in additional_plugin %}compress.init_app(app){% endif %}     
    {% if database != "none"%}from .model.user import User{% endif %}
    {% if auth == "flask-login" %}
    # login manager
    login_manager = LoginManager()
    login_manager.login_view = "your login view"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(id))
    {% endif %}
    
    return app