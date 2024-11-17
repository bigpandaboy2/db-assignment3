from flask import Blueprint

doctor = Blueprint('doctor', __name__)

from health_info.doctor import routes
