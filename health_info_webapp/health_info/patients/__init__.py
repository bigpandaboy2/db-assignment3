from flask import Blueprint

patients = Blueprint('patients', __name__)

from health_info.patients import routes