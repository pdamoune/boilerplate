import os


class Config:
    # Secret key
    SECRET_KEY = os.environ.get('SECRET_KEY')\
        or 'set $SECRET_KEY'

    # Admin account
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')\
        or 'set $ADMIN_EMAIL'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')\
        or 'set $ADMIN_PASSWORD'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    print(" + [DB] " + SQLALCHEMY_DATABASE_URI)
    JSONIFY_PRETTYPRINT_REGULAR = True
    TEMPLATES_AUTO_RELOAD = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


config = {
    'development': DevelopmentConfig,
    'test': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
