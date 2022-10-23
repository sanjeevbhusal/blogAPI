import sys

from flask import Blueprint

print("app" in sys.modules)
user = Blueprint("user", __name__)