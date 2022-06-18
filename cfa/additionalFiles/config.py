class Config(object):
    DEBUG = True
    ENV = "development"
    
    SECRET_KEY = "{{generate_key(50)}}"
    SECURITY_PASSWORD_SALT = "{{generate_key(50)}}"
    
    {% if database == "flask-jwt-extended"%} JWT_SECRET_KEY = "{{generate_key(50)}}"{% endif%}    
    {% if database == "mysql"%}SQLALCHEMY_DATABASE_URI = "mysql+pymysql://user:pass@host/database"{% elif database == "postgresql"%}SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://user:pass@host:port/database"{% else %}SQLALCHEMY_DATABASE_URI = "sqlite://dbase.db"{% endif %}
    SQLALCHEMY_TRACK_MODIFICATIONS = False