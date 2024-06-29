from datetime import timedelta


class _BaseConfig:
    API_TITLE = "London Economic Today"
    API_VERSION = None

    # flask-smorest
    OPENAPI_VERSION = "3.1.0"
    OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_URL_PREFIX = "/api/docs"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    API_SPEC_OPTIONS = {
        "components": {
            "securitySchemes": {
                "Bearer Auth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization",
                    "bearerFormat": "JWT",
                    "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token",
                }
            }
        },
    }


class AppBaseConfig(_BaseConfig):
    # flask-sqlalchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.sqlite"

    # flask-jwt-extended
    JWT_SECRET_KEY = "should-be-a-secret"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
