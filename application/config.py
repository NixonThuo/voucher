from urllib.parse import quote_plus as urlquote


class Config(object):
    HOST = "0.0.0.0"
    SECRET_KEY = "randomstuff"
    DB_USERNAME = "postgres"
    DB_PASSWORD = urlquote("colorsoftheworld")
    SESSION_COOKIE_SECURE = False
    POSTGRES_URL = "45.80.152.117"
    POSTGRES_DB = "thabiso"
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}?application_name=H3SIMPLE'.format(
        user=DB_USERNAME, pw=DB_PASSWORD, url=POSTGRES_URL,
        db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 30
    SQLALCHEMY_MAX_OVERFLOW = 40
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_BINDS = {
        'maindb': SQLALCHEMY_DATABASE_URI
    }


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    pass


class DevelopmentConfig(Config):
    pass
