import marshmallow as ma

from . import hello_bp


class MsgSchema(ma.Schema):
    msg = ma.fields.String()


@hello_bp.route('')
@hello_bp.response(200, MsgSchema)
def hello():
    """A hello world message"""
    return {'msg': 'Welcome to the London Economic Today API v1'}
