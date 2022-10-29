"""
All the blueprints which are to be registered by the flask app instance are exported from this module
"""

from blog_api.blueprints.comment import comment
from blog_api.blueprints.like import like
from blog_api.blueprints.post import post
from blog_api.blueprints.user import user
