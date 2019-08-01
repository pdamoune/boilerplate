import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Secret key
    SECRET_KEY = os.environ.get('SECRET_KEY')\
        or 'set $SECRET_KEY'

    # Admin account
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')\
        or 'set $ADMIN_EMAIL'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')\
        or 'set $ADMIN_PASSWORD'

    # Mail setting
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    print(" + [DB] " + SQLALCHEMY_DATABASE_URI)
    JSONIFY_PRETTYPRINT_REGULAR = True
    # Useless ?
    # TEMPLATES_AUTO_RELOAD = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
