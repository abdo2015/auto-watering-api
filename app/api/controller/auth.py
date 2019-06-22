from flask import request
from flask_restplus import Namespace, Resource, fields
from flask_login import login_user, logout_user, login_required

from ..model.user import User

app = Namespace('auth', 'endpoints for login and logout users')
user_auth = app.model("auth", {
    'email': fields.String(required=True, description='user email address'),
    'password': fields.String(required=True, description="user password")
})

# TODO validate request data
@app.route('/login')
@app.expect(user_auth)
class Login(Resource):
    def post(self):
        try:
            data = request.json
            email = data.get('email')
            password = data.get('password')
            user = User.query.filter_by(email=email).first()
            if not (user and user.check_password(password)):
                response_opj = {
                    'status': 'faild',
                    'message': 'Email or password is wrong'
                }
                return response_opj, 401

            response_opj = {
                'status': 'success',
                'message': 'Successfully logged in'
            }
            login_user(user)
            return response_opj, 200
        except Exception as e:
            print("Exception at login:", str(e))
            response_opj = {
                'status': 'faild',
                'message': 'Something Wrong, please try again later'
            }
            return response_opj, 500

# TODO validate request data
@app.route('/logout')
class Logout(Resource):
    @login_required
    def get(self):
        try:
            logout_user()
            response_opj = {
                "status": "success",
                "message": "Successfully logged out"
            }
            return response_opj, 200
        except Exception as e:
            print("Exception at logout:", str(e))
            response_opj = {
                'status': 'faild',
                'message': 'Something Wrong, please try again later'
            }
            return response_opj, 500


# TODO delete test class
@app.route('/test')
class Test(Resource):
    @login_required
    def get(self):
        return "worked"
