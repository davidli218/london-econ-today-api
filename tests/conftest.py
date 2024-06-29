import os
import tempfile

import pytest

from app import create_app


class AuthActions:
    source_url = '/api/v1/auth/token'

    def __init__(self, client):
        self._client = client

    def login(self, email='pyteset@test.com', password='pytest-123456'):
        return self._client.post(self.source_url, json={'email': email, 'password': password})

    def revoke(self, token):
        return self._client.delete(self.source_url, headers={'Authorization': f'Bearer {token}'})

    def refresh(self, refresh_token):
        return self._client.put(self.source_url, headers={'Authorization': f'Bearer {refresh_token}'})

    def status(self, access_token):
        return self._client.get(self.source_url, headers={'Authorization': f'Bearer {access_token}'})

    @staticmethod
    def header(access_token):
        return {'Authorization': f'Bearer {access_token}'}


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
    })

    from app.extensions import db
    with app.app_context():
        from tests.data_sql import import_test_data
        import_test_data()

    yield app

    with app.app_context():
        db.engine.dispose()

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def auth(client):
    return AuthActions(client)
