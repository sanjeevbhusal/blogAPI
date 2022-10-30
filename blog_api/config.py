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


class TestingConfiguration:
    """
    Testing Configuration
    """

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URL") or "sqlite:///test_database.db"
    )
    TESTING = True
    SERVER_NAME = "localhost"
