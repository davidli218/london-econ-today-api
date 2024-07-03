from flask_smorest import Blueprint

# Define the blueprints
auth_bp = Blueprint('auth', __name__)
dataset_bp = Blueprint('dataset', __name__)
hello_bp = Blueprint('hello', __name__)
user_bp = Blueprint('user', __name__)

# Register the routes to the blueprints
from app.routes import (
    hello,
    dataset,
    auth,
    user,
    subscription,
)  # noqa


def register_blueprints(api):
    api.register_blueprint(hello_bp, url_prefix='/api/v1')
    api.register_blueprint(dataset_bp, url_prefix='/api/v1/dataset')
    api.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    api.register_blueprint(user_bp, url_prefix='/api/v1/user')
