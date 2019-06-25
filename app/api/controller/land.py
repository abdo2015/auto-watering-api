import datetime
from flask import request
from flask_restplus import Namespace, Resource, fields
from flask_login import login_required, current_user
from flask_expects_json import expects_json

from ..model.user import User
from ..model.land import Land

from ... import db

app = Namespace('land', 'Lands endpoints (CRUD)')
land_dto = app.model("new land", {
    'land_area': fields.Float(required=True, description='land area, should be positive number'),
    'plant_id': fields.Integer(description='Plant id')
})
update_dto = app.model('update land', {
    'land_area': fields.Float(required=True, description='land area, should be positive number'),
    'id': fields.Integer(required=True, description="land ID"),
    'plant_id': fields.Integer(description='Plant id')

})
del_dto = app.model('delete land', {
    'id': fields.Integer(required=True, description="land ID")
})

post_schema = {
    'type': 'object',
    'properties': {
        'land_area': {'type': 'number'},
        'plant_id': {'type': 'integer'}
    },
    'required': ['land_area']
}

put_schema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer'},
        'land_area': {'type': 'number'},
        'plant_id': {'type': 'integer'}
    },
    'required': ['id', 'land_area']
}

del_schema = {
    'type': 'object',
    'properties': {
        'id': {'type', 'integer'}
    },
    'required': ['id']
}


@app.route('/new')
class AddLand(Resource):
    @login_required
    @app.expect(land_dto)
    @expects_json(post_schema)
    def post(self):
        try:
            data = request.json
            user = User.query.filter_by(email=current_user.email).first()
            land_area = data.get('land_area')
            owner_id = user.id
            land = Land(land_area=land_area, owner_id=owner_id)
            plant_id = data.get('plant_id') or None
            if plant_id:
                land.plant_id = plant_id
            db.session.add(land)
            db.session.commit()
            response_opj = {
                "status": "success",
                "message": "Successfully add land"
            }
            return response_opj, 200

        except ValueError as e:
            response_opj = {
                'status': 'faild',
                'message': str(e)
            }
            return response_opj, 422
        except Exception as e:
            print("error at add land : ", e)
            response_opj = {
                'status': 'faild',
                'message': 'Something Wrong, please try again later'
            }
            return response_opj, 500


@app.route('/update')
class Update(Resource):
    @login_required
    @app.expect(update_dto)
    @expects_json(put_schema)
    def put(self):
        try:
            data = request.json
            land_id = data.get('id')
            land = Land.query.filter_by(id=land_id).first()
            if not land:
                response_opj = {
                    'status': 'faild',
                    'message': f'No land has id:{land_id}'
                }
                return response_opj, 422
            land.land_area = data.get('land_area')
            plant_id = data.get('plant_id') or None
            if plant_id:
                land.plant_id = plant_id
            db.session.add(land)
            db.session.commit()
            response_opj = {
                "status": "success",
                "message": "Successfully update land"
            }
            return response_opj, 200
        except ValueError as e:
            response_opj = {
                'status': 'faild',
                'message': str(e)
            }
            return response_opj, 422

        except Exception as e:
            print('Error at update land:', e)
            response_opj = {
                'status': 'faild',
                'message': 'Something Wrong, please try again later'
            }
            return response_opj, 500


@app.route('/delete')
class Delete(Resource):
    @expects_json(del_schema)
    def delete(self):
        try:
            data = request.json
            land_id = data.get('id')
            land = Land.query.get(land_id)
            if not land:
                response_opj = {
                    'status': 'faild',
                    'message': f'No land has id:{land_id}'
                }
                return response_opj, 422
            db.session.delete(land)
            db.session.commit()
            response_opj = {
                "status": "success",
                "message": "Successfully delete land"
            }
            return response_opj, 200
        except Exception as e:
            print('Error at update land:', e)
            response_opj = {
                'status': 'faild',
                'message': 'Something Wrong, please try again later'
            }
            return response_opj, 500
