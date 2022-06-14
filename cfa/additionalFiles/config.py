class Config(object):
    DEBUG = True
    ENV = "development"
    
    SECREET_KEY = "some random string"
    SECURITY_PASSWORD_SALT = "random string that different from SECRET_KEY"
    
    {% if database == "mysql"%}
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://user:pass@host/database"
    {% else %}
    SQLALCHEMY_DATABASE_URI = "sqlite://dbase.db"
    {% endif %}
    SQLALCHEMY_TRACK_MODIFICATIONS = False