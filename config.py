import datetime
import os
import app

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY") or "alidugyhniuvmsfdijshHAKJLWIU3029091IOEASHDJFoisjdfl;ahgihawelfjadiowf;kaqkl;HAKJLWDFJKASHDJF"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = ";laksdj78906f;ka143whe23423;ufaj3sdnf5OA2J4dglarjA1DGehk523fnkadslS23ADFbfguew;hf124jgadl"
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=24)
    #mail configuration
    MAIL_SERVER = 'smtp-relay.sendinblue.com'
    MAIL_PORT = 2525
    # MAIL_USE_TLS = True
    MAIL_USERNAME = 'tradeasynotifs@gmail.com'
    MAIL_PASSWORD = 'ZNVhb8UfFA2H5EsW'
    MAIL_DEFAULT_SENDER = 'tradeasynotifs@gmail.com'
    # MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    # MAIL_PORT = 2525
    # MAIL_USERNAME = '2f9b315d5925d7'
    # MAIL_PASSWORD = '6a53c14cbefa25'
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:password@tradeeasy-postgres.cmvvqltryuil.us-east-1.rds.amazonaws.com"


# class TestingConfig(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or \
#                               "sqlite://"
#
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:password@tradeeasy-postgres.cmvvqltryuil.us-east-1.rds.amazonaws.com"


config = {
    "development": DevelopmentConfig,
    # "testing": TestingConfig,
    "production": ProductionConfig,
    "default": ProductionConfig
}


