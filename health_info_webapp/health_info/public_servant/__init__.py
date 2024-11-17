from flask import Blueprint

public_servant = Blueprint('public_servant', __name__)

from health_info.public_servant import routes
