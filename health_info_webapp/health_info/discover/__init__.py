from flask import Blueprint

discover = Blueprint('discover', __name__)

from health_info.discover import routes
