from flask.views import MethodView
from flask_jwt_extended import current_user
from flask_smorest import abort
from flask_smorest.error_handler import ErrorSchema

from app.extensions import db
from app.extensions import jwt_required_with_oas
from app.models import SubscriptionModel
from . import user_bp


@user_bp.route('/<int:uid>/subscription', endpoint='subscription')
class UserSubscription(MethodView):
    @staticmethod
    @jwt_required_with_oas()
    @user_bp.response(201)
    @user_bp.alt_response(409, schema=ErrorSchema, description='User already has a subscription')
    def post(uid):
        """Create a subscription for the user"""
        if current_user.uid != uid:
            abort(401, message='Unauthorized')

        if current_user.subscription is not None:
            abort(409, message='User already has a subscription')

        db.session.add(SubscriptionModel(user_id=uid))
        db.session.commit()

    @staticmethod
    @jwt_required_with_oas()
    @user_bp.response(204)
    @user_bp.alt_response(409, schema=ErrorSchema, description='User does not have a subscription')
    def delete(uid):
        """Cancel the subscription of the user"""
        if current_user.uid != uid:
            abort(401, message='Unauthorized')

        if current_user.subscription is None:
            abort(409, message='User does not have a subscription')

        db.session.add(current_user.subscription.to_recycled())
        db.session.delete(current_user.subscription)
        db.session.commit()
