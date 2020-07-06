from flask import request
from flask_restplus import Resource

from app.main.service.auth_helper import Auth
from ..util.dto import AuthDto

api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    @api.doc('user login')
    @api.response(400, 'Email or password incorrect.')
    @api.expect(user_auth, validate=True)
    def post(self):
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/adminLogin')
class UserLogin(Resource):
    @api.doc('admin login')
    @api.response(400, 'Email or password incorrect.')
    @api.expect(user_auth, validate=True)
    def post(self):
        post_data = request.json
        return Auth.login_admin_user(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    @api.doc('logout a user')
    def post(self):
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)


@api.route('/isUserAlreadyLogged')
class IsUserAlreadyLogged(Resource):
    @api.doc('Is user already logged ?')
    @api.response(200, 'User id.')
    @api.response(404, 'Unknown user.')
    def get(self):
        response, status = Auth.get_logged_in_user(request)
        if status == 200:
            response_object = {
                'id': response.get('data').id
            }
            return response_object
        else:
            api.abort(404, 'User not found')
