from flask import Blueprint

specialize = Blueprint('specialize', __name__)

from health_info.specialize import routes