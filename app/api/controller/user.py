import datetime
from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields
from flask_login import login_user, login_required, current_user
from flask_expects_json import expects_json

from ..model.user import User
from ..model.land import Land

from ... import db

app = Namespace('user', 'add and update users endpoints')
user_dto = app.model("user", {
    'email': fields.String(required=True, description='user email address'),
    'password': fields.String(required=True, description="user password"),
    'username': fields.String(required=True, description="user name")
})

schema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'email': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['email', 'password', 'username']
}


@app.route('/singup')
class SignUp(Resource):
    @app.expect(user_dto)
    @expects_json(schema)
    def post(self):
        try:
            data = request.json
            email = data.get('email')
            user = User.query.filter_by(email=email).first()
            if user:
                response_opj = {
                    'status': 'faild',
                    'message': 'user already exist, please login.'
                }
                return response_opj, 409
            password = data.get('password')
            username = data.get('username')
            registered_on = datetime.datetime.utcnow()
            user = User(email=email, password=password,
                        username=username, registered_on=registered_on)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            response_opj = {
                'status': 'success',
                'message': 'User successfully signed up and logged in.'
            }
            return response_opj, 201
        except Exception as e:
            print(e)
            response_opj = {
                'status': 'faild',
                'message': 'Something Wrong, please try again later.'
            }
            return response_opj, 500


@app.route('/update')
class UpdateUser(Resource):
    @app.expect(user_dto)
    @login_required
    @expects_json(schema)
    def put(self):
        try:
            data = request.json
            user = User.query.filter_by(email=current_user.email).first()
            if not user:
                response_opj = {
                    'status': 'faild',
                    'message': 'Something Wrong, please try again later'
                }
                return response_opj, 500
            user.email = data.get('email')
            user = User.query.filter_by(email=data.get('email')).first()
            if user:
                response_opj = {
                    'status': 'faild',
                    'message': f'Email : {data.get('email')} already exist'
                }
                return response_opj, 409
            user.password = data.get('password')
            user.username = data.get('username')
            db.session.add(user)
            db.session.commit()
            response_opj = {
                "status": "success",
                "message": "Successfully update user data"
            }
            return response_opj, 200
        except Exception as e:
            print("Exception at logout:", str(e))
            response_opj = {
                'status': 'faild',
                'message': 'Something Wrong, please try again later'
            }
            return response_opj, 500


@app.route('/lands')
class UserLands(Resource):
    @login_required
    def get(self):
        user_id = current_user.id
        lands = Land.query.filter_by(owner_id=user_id).all()
        if not lands:
            response_opj = {
                'status': 'success',
                'message': "user don't have any lands right now"
            }
            return response_opj, 200
        response_opj = {
            'status': 'success',
            "data": [land.serialize for land in lands]
        }
        return response_opj, 200
