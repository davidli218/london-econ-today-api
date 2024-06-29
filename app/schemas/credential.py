import marshmallow as ma


class TokenSchema(ma.Schema):
    access_token = ma.fields.String(required=True)
    refresh_token = ma.fields.String()


class TokenStatusSchema(ma.Schema):
    is_fresh = ma.fields.Boolean(required=True)


class UserAuthArgSchema(ma.Schema):
    email = ma.fields.Email(required=True)
    password = ma.fields.String(required=True)
