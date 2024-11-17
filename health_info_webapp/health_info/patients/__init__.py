from flask import Blueprint

patients = Blueprint('patients', __name__, template_folder='../templates')

from health_info.patients import routes