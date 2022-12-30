from flask import Blueprint

auth = Blueprint('auth', __name__)

from EMS.auth import views
