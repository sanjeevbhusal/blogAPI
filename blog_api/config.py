import os


class DevelopmentConfiguration:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///dev_database.db'


class TestingConfiguration:
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///test_database.db'
    TESTING = True
    SERVER_NAME = "localhost"
