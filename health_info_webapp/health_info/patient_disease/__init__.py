from flask import Blueprint

patient_disease = Blueprint('patient_disease', __name__)

from health_info.patient_disease import routes
