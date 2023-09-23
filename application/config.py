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
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'echo_pool': True
    }
    SQLALCHEMY_BINDS = {
        'maindb': DB_URL
    }


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    pass


class DevelopmentConfig(Config):
    pass
