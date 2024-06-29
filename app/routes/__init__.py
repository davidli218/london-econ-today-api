from flask_smorest import Blueprint

auth_bp = Blueprint('auth', __name__)
dataset_bp = Blueprint('dataset', __name__)
hello_bp = Blueprint('hello', __name__)
user_bp = Blueprint('user', __name__)

from . import hello  # noqa
from . import dataset  # noqa
from . import auth  # noqa
from . import user  # noqa
from . import subscription  # noqa
