from flask import Blueprint
from flask_restful import Api

# Create API v1 blueprint and API object
api_v1 = Blueprint('api_v1', __name__)
api = Api(api_v1)

# Import resource classes and add them to the API with URLs
from app.api.v1.routes import auth

# Assuming auth contains resource classes, register them here; for example:
# api.add_resource(auth.AuthResource, '/auth')
# Adjust the above line depending on your auth.py definitions
