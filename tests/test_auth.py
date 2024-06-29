import pytest


def test_get_new_token(auth):
    login_response = auth.login()

    # 1. Check the response status code is 201 CREATED
    assert login_response.status_code == 201

    # 2. Check the response contains the expected fields
    assert set(login_response.json.keys()) == {'access_token', 'refresh_token'}
    assert login_response.json['access_token']
    assert login_response.json['refresh_token']

    # 3. Check the response contains expected access token
    token_status_response = auth.status(login_response.json['access_token'])
    refresh_token_status_response = auth.status(login_response.json['refresh_token'])
    assert token_status_response.status_code == 200
    assert refresh_token_status_response.status_code == 200
    assert token_status_response.json['is_fresh']

    # 4. Check the invalid credentials return 401 UNAUTHORIZED
    assert auth.login(email='xxx@xxx.com', password='xxx').status_code == 401

    # 5. Check the invalid requests return 422 UNPROCESSABLE ENTITY
    assert auth.login(email='xxx', password='xxx').status_code == 422
    assert auth.login(email='xxx', password=None).status_code == 422
    assert auth.login(email=None, password='xxx').status_code == 422


@pytest.mark.parametrize(('login_args', 'status_code'), (
        ({'email': 'xxx', 'password': 'xxx'}, 422),  # invalid email format should return 422
        ({'email': 'xxx@xxx.com', 'password': 'xxxx-xxxx'}, 401),  # invalid credentials should return 401
        ({'email': 'donald@duck.com', 'password': 'xxxx-xxxx'}, 401),  # invalid credentials should return 401
))
def test_get_new_token_fail(auth, login_args, status_code):
    assert auth.login(**login_args).status_code == status_code


def test_refresh_token(auth):
    refresh_token_response = auth.refresh(auth.login().json['refresh_token'])

    # 1. Check the refresh token is valid
    assert refresh_token_response.status_code == 201

    # 2. Check the response contains the expected fields
    assert set(refresh_token_response.json.keys()) == {'access_token', 'refresh_token'}

    # 3. Check the new access token is valid and not fresh
    new_token_status_response = auth.status(refresh_token_response.json['access_token'])
    assert new_token_status_response.status_code == 200
    assert not new_token_status_response.json['is_fresh']

    # 4. Check the invalid refresh token return 422 UNPROCESSABLE ENTITY
    assert auth.refresh('xxx').status_code == 422


def test_token_status(auth):
    login_response = auth.login()
    access_token = login_response.json['access_token']
    refresh_token = login_response.json['refresh_token']

    # 1. Check the valid token return 200 OK
    assert auth.status(access_token).status_code == 200
    assert auth.status(refresh_token).status_code == 200

    # 2. Check the invalid token return 422 UNPROCESSABLE ENTITY
    assert auth.status('xxx').status_code == 422


def test_revoke_token(auth):
    login_response = auth.login()
    access_token = login_response.json['access_token']
    refresh_token = login_response.json['refresh_token']

    # 1. Check the tokens are valid before revoking
    assert auth.status(access_token).status_code == 200
    assert auth.status(refresh_token).status_code == 200

    # 2. Check the valid token return 200 OK
    assert auth.revoke(access_token).status_code == 204
    assert auth.revoke(refresh_token).status_code == 204

    # 3. Check the token is revoked and return 401 UNAUTHORIZED
    assert auth.status(access_token).status_code == 401
    assert auth.status(refresh_token).status_code == 401

    # 4. Check the invalid token return 422 UNPROCESSABLE ENTITY
    assert auth.revoke('xxx').status_code == 422
