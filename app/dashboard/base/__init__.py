from flask import Blueprint

blueprint = Blueprint(
    'base_blueprint',
    __name__,
    url_prefix='/dashboard',
    template_folder='templates',
    static_folder='static'
)
