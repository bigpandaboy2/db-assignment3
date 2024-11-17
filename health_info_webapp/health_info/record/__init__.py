from flask import Blueprint

record = Blueprint('record', __name__)

from health_info.record import routes
