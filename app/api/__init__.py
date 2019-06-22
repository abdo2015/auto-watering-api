from flask import Blueprint
from flask_restplus import Api

from app.api.controller.auth import app as auth_ns
from app.api.controller.user import app as user_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title="Api for auto watering system",
          version='1.0',
          description="handle all web app requests and arduino requests",
          doc='/api'
          )

api.add_namespace(auth_ns)
api.add_namespace(user_ns)
