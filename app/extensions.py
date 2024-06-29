from copy import deepcopy
from functools import wraps

from argon2 import PasswordHasher  # noqa
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

api = Api()
db = SQLAlchemy()
jwt = JWTManager()
ph = PasswordHasher()

from app import models  # noqa
from flask_jwt_extended import jwt_required  # noqa


def jwt_required_with_oas(*args, **kwargs):
    """Overwrite the jwt_required decorator to add openapi doc support."""

    # noinspection PyProtectedMember
    def decorator(func):
        @wraps(func)
        def wrapper(*f_args, **f_kwargs):
            return jwt_required(*args, **kwargs)(func)(*f_args, **f_kwargs)

        # Add the security information to the openapi doc
        wrapper._apidoc = deepcopy(getattr(func, "_apidoc", {}))
        wrapper._apidoc.setdefault('manual_doc', {})
        wrapper._apidoc['manual_doc']['security'] = [{"Bearer Auth": []}]

        # Add the 401 response to the openapi doc
        wrapper._apidoc['manual_doc'].setdefault('responses', {})
        wrapper._apidoc['manual_doc']['responses'][401] = {
            'description': 'Unauthorized',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            "msg": {  # current_app.config["JWT_ERROR_MESSAGE_KEY"]
                                'type': 'string',
                                'example': 'Unauthorized'
                            }
                        }
                    }
                }
            }
        }

        return wrapper

    return decorator


@jwt.user_identity_loader
def user_identity_lookup(user):
    """
    This function will be called when creating tokens.
    """
    return user.uid


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """
    This function will be called when you access the current_user proxy.
    """
    identity = jwt_data['sub']

    return db.session.execute(
        db.select(models.UserModel).where(models.UserModel.uid == identity)
    ).scalar_one_or_none()


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    """
    This function will be called when checking if a token is blacklisted.
    """
    _, jti = jwt_header, jwt_payload['jti']

    token = db.session.execute(
        db.select(models.TokenBlocklistModel).where(models.TokenBlocklistModel.jti == jti)
    ).scalar_one_or_none()

    return token is not None
