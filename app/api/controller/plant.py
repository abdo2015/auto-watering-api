from flask_login import login_required
from flask_restplus import Namespace, Resource, fields
from ..model.land import Plant

from ... import db

app = Namespace('plant', 'use to get available plant')
plant_dto = app.model("user", {
    'name': fields.String(required=True, description='plant name'),
    'water_amount': fields.Float(required=True, description="amount of water plant need"),
    'fertilizer': fields.String(required=True, description="name if fertilizer plant need")
})

schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'water_amount': {'type': 'number'},
        'fertilizer': {'type': 'string'}

    },
    'required': ['name', 'water_amount', 'fertilizer']
}


@app.route('')
class AllPlants(Resource):
    # @login_required
    @app.expect(plant_dto)
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
