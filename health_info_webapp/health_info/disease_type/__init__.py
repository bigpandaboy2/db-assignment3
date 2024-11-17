from flask import Blueprint

disease_type = Blueprint('disease_type', __name__)

from health_info.disease_type import routes
