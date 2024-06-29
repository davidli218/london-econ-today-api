import marshmallow as ma

from flask import url_for
from marshmallow import validate


class UserRegInfoArgSchema(ma.Schema):
    email = ma.fields.Email(required=True)
    password = ma.fields.String(required=True, validate=validate.Length(min=8, max=36))
    name = ma.fields.String(load_default='', validate=validate.Length(max=20))


class UserUpdateInfoArgSchema(ma.Schema):
    email = ma.fields.Email()
    password = ma.fields.String(validate=validate.Length(min=8, max=36))
    name = ma.fields.String(validate=validate.Length(min=1, max=20))


class UserInfoSchema(ma.Schema):
    name = ma.fields.String()
    email = ma.fields.String()
    registered_on = ma.fields.DateTime(format='iso8601')

    is_subscribed = ma.fields.Function(lambda user: user.subscription is not None)
    uri = ma.fields.Function(lambda obj: url_for('user.info', uid=obj.uid, _external=True))


class UserInfoNoUriSchema(UserInfoSchema):
    class Meta:
        exclude = ('uri',)
