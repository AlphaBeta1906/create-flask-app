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