from flask.views import MethodView
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import current_user
from flask_jwt_extended import get_jwt
from flask_smorest import abort

from app.extensions import db
from app.extensions import jwt_required_with_oas
from app.models import TokenBlocklistModel
from app.models import UserModel
from app.schemas.credential import TokenSchema
from app.schemas.credential import TokenStatusSchema
from app.schemas.credential import UserAuthArgSchema
from . import auth_bp


@auth_bp.route('/token', endpoint='token')
class Token(MethodView):
    @jwt_required_with_oas(verify_type=False)
    @auth_bp.response(200, TokenStatusSchema)
    def get(self):
        """Get the token status"""
        return {
            'is_fresh': get_jwt()['fresh']
        }

    @auth_bp.arguments(UserAuthArgSchema, location='json')
    @auth_bp.response(201, TokenSchema)
    def post(self, args: dict):
        """Create a new pair of tokens"""
        arg_email, arg_password = args['email'], args['password']

        user = db.session.execute(
            db.select(UserModel).where(UserModel.email == arg_email)
        ).scalar_one_or_none()

        if user is None or not user.verify_password(arg_password):
            abort(401, message='Unauthorized')

        # If the hash's parameters and if outdated, rehash the password
        if user.is_password_weak():
            user.password = arg_password
            db.session.commit()

        access_token = create_access_token(identity=user, fresh=True)
        refresh_token = create_refresh_token(identity=user)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    @jwt_required_with_oas(refresh=True)
    @auth_bp.response(201, TokenSchema)
    def put(self):
        """Create a new access token using the refresh token"""
        return {
            'access_token': create_access_token(identity=current_user, fresh=False),
            'refresh_token': get_jwt()['jti']
        }

    @jwt_required_with_oas(verify_type=False)
    @auth_bp.response(204)
    def delete(self):
        """Revoke a token"""
        token = TokenBlocklistModel(jti=get_jwt()['jti'], revoked_at=db.func.now())
        db.session.add(token)
        db.session.commit()
