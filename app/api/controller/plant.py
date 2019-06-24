from flask_login import login_required
from flask_restplus import Namespace, Resource
from ..model.land import Plant

from ... import db

app = Namespace('plant', 'use to get available plant')


@app.route('')
class AllPlants(Resource):
    @login_required
    def get(self):
        plants = Plant.query.order_by('name').all()
        if not plants:
            response_opj = {
                'status': 'success',
                'message': "we don't have any avilable plant right now!"
            }
            return response_opj, 200

        response_opj = {
            'status': 'success',
            'plants': [dict(id=plant.id, name=plant.name) for plant in plants]
        }
        return response_opj, 200
