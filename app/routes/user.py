from flask.views import MethodView
from flask_jwt_extended import current_user
from flask_smorest import abort
from flask_smorest.error_handler import ErrorSchema

from app.extensions import db
from app.extensions import jwt_required_with_oas
from app.models import UserModel
from app.schemas.user import UserInfoNoUriSchema
from app.schemas.user import UserInfoSchema
from app.schemas.user import UserRegInfoArgSchema
from app.schemas.user import UserUpdateInfoArgSchema
from . import user_bp


@user_bp.route('', endpoint='signup')
class Users(MethodView):
    @user_bp.arguments(UserRegInfoArgSchema, location='json')
    @user_bp.response(201, UserInfoSchema(only=['email', 'uri']))
    @user_bp.alt_response(409, schema=ErrorSchema, description='User already exists')
    def post(self, args):
        """Create a new user"""
        if db.session.execute(db.select(UserModel).where(UserModel.email == args['email'])).scalar() is not None:
            abort(409, message='User already exists')

        user = UserModel(
            email=args['email'],
            password=args['password'],
            name=args['name'] if len(args['name']) > 0 else args['email'].split('@')[0][:12]
        )

        db.session.add(user)
        db.session.commit()

        return user


@user_bp.route('/<int:uid>', endpoint='info')
class User(MethodView):
    @jwt_required_with_oas()
    @user_bp.response(200, UserInfoNoUriSchema)
    def get(self, uid):
        """Get user info by uid"""
        if current_user.uid != uid:
            abort(401, message='Unauthorized')

        return current_user

    @jwt_required_with_oas(fresh=True)
    @user_bp.arguments(UserUpdateInfoArgSchema, location='json')
    @user_bp.response(200, UserInfoNoUriSchema)
    @user_bp.alt_response(409, schema=ErrorSchema, description='Email already exists')
    def put(self, args, uid):
        """Update user info by uid"""
        if current_user.uid != uid:
            abort(401, message='Unauthorized')

        if args.get('email') and args['email'] != current_user.email:
            if db.session.execute(db.select(UserModel).where(UserModel.email == args['email'])).scalar() is not None:
                abort(409, message='Email already exists')

            current_user.email = args['email']

        if args.get('password'):
            current_user.password = args['password']

        if args.get('name'):
            current_user.name = args['name']

        db.session.commit()

        return current_user

    @staticmethod
    @jwt_required_with_oas(fresh=True)
    @user_bp.response(204)
    def delete(uid):
        """Delete user by uid"""
        if current_user.uid != uid:
            abort(401, message='Unauthorized')

        if current_user.subscription is not None:
            db.session.add(current_user.subscription.to_recycled())
            db.session.delete(current_user.subscription)

        db.session.add(current_user.to_recycled())
        db.session.delete(current_user)
        db.session.commit()
