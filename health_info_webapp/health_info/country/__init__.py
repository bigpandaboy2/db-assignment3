from flask import Blueprint

country = Blueprint('country', __name__)

from health_info.country import routes
