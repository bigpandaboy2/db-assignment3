from flask import Blueprint

disease = Blueprint('disease', __name__)

from health_info.disease import routes
