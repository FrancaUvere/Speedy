from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")


from api.v1.views.users import *
from api.v1.views.customers import *
from api.v1.views.error_handler import *
from api.v1.views.accounts import *
from api.v1.views.transactions import *
