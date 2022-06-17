from flask import Flask
{% if "flask-sqlalchemy" in additional_plugin %}from flask_sqlalchemy import SQLAlchemy{% endif %}
{% if "flask-cors" in additional_plugin %}from flask_cors import CORS{% endif %}