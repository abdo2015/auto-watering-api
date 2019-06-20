from flask import Blueprint
from flask_restplus import Api

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title="Api for auto watering system",
          version='1.0',
          description="handle all web app requests and arduino requests",
          doc='/api'
          )
