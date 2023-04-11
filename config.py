import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY") or "alidugyhniuvmsfdijshHAKJLWIU3029091IOEASHDJFoisjdfl;ahgihawelfjadiowf;kaqkl;HAKJLWDFJKASHDJF"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = ";laksdj78906f;ka143whe23423;ufaj3sdnf5OA2J4dglarjA1DGehk523fnkadslS23ADFbfguew;hf124jgadl"
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=24)

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


