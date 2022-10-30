"""
Configuration for multiple stages of development like development, testing and production
"""

import os


class DevelopmentConfiguration:
    """
    Development Configuration
    """

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DEV_DATABASE_URL") or "sqlite:///dev_database.db"
    )
    DEFAULT_SECRET_KEY = (
        "5eb30aa701fb814dd284b26cc9a9c251"  # used when user doesnot set a secret key
    )


class TestingConfiguration:
    """
    Testing Configuration
    """

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URL") or "sqlite:///test_database.db"
    )
    TESTING = True
    SERVER_NAME = "localhost"
