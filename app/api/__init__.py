from flask import Blueprint
from flask_restplus import Api

from app.api.controller.auth import app as auth_ns
from app.api.controller.user import app as user_ns
from app.api.controller.land import app as land_ns
from app.api.controller.plant import app as plant_ns


blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title="Api for auto watering system",
          version='1.0',
          description="handle all web app requests and arduino requests",
          doc='/'
          )

api.add_namespace(auth_ns)
api.add_namespace(user_ns)
api.add_namespace(land_ns)
api.add_namespace(plant_ns)
