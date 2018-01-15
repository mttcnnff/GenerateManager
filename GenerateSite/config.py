import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    TOKEN_EXPIRATION = 3600
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MATTER_MAIL_SUBJECT_PREFIX = '[Matter]'
    MATTER_MAIL_SENDER = 'Matter Admin <mttcnnff@gmail.com>'
    MATTER_ADMIN = os.environ.get('MATTER_ADMIN') or 'mttcnnff@gmail.com'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING =True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development' : DevelopmentConig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
    'default' : DevelopmentConig
}

