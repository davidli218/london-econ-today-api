import pytest

from app.extensions import db
from app.models import SubscriptionRecycledModel
from app.models import UserModel
from app.models import UserRecycledModel

register_url = '/api/v1/user'
info_url = '/api/v1/user/{uid}'


@pytest.mark.parametrize('register_data', (
        {'name': 'test_user_001', 'email': 'test_user_001@test.com', 'password': 'test_password'},
        {'name': '', 'email': 'test_user_002@test.com', 'password': 'test_password'},
))
def test_register_user(app, client, auth, register_data):
    response = client.post(register_url, json=register_data)
    token = auth.login(register_data['email'], register_data['password']).json['access_token']

    # 1. Check that the response status code is 201 CREATED
    assert response.status_code == 201

    # 2. Check that the response contains the expected fields
    assert set(response.json.keys()) == {'email', 'uri'}

    # 3. Check that the response.uri is valid
    assert client.get(response.json['uri'], headers=auth.header(token)).status_code == 200

    # 4. Check that the user is created in the database
    with app.app_context():
        assert db.session.execute(
            db.select(UserModel).where(UserModel.email == register_data['email'])
        ).scalar_one_or_none() is not None

    # 5. Check email is unique
    assert client.post(register_url, json=register_data).status_code == 409


@pytest.mark.parametrize('register_data', (
        {'name': 'xx_xxx', 'email': 'xxxx_xxxx_xxxx', 'password': 'x' * 12},  # Email is not valid
        {'name': 'xx_xxx', 'email': 'xxxxxx@xxx.com', 'password': 'x' * 4},  # Password is too short
        {'name': 'xx_xxx', 'email': 'xxxxxx@xxx.com', 'password': 'x' * 40},  # Password is too long
        {'name': 'x' * 40, 'email': 'xxxxxx@xxx.com', 'password': 'x' * 12},  # Name is too long
))
def test_register_user_invalid_data(app, client, register_data):
    # 1. Check that the response status code is 422 UNPROCESSABLE ENTITY
    assert client.post(register_url, json=register_data).status_code == 422


def test_register_user_invalid_json(app, client):
    # 1. Check missing data for required field returns 422 UNPROCESSABLE ENTITY
    assert client.post(register_url, json={}).status_code == 422
    assert client.post(register_url, json={'name': 'test_user_001'}).status_code == 422

    # 2. Check invalid JSON returns 400 BAD REQUEST
    assert client.post(register_url, data='invalid json', content_type='application/json').status_code == 400


def test_register_user_invalid_method(app, client):
    assert client.get(register_url).status_code == 405
    assert client.put(register_url).status_code == 405
    assert client.delete(register_url).status_code == 405


def test_user_data_privacy(client, auth):
    token = auth.login('pyteset@test.com', 'pytest-123456').json['access_token']
    new_info = {'name': 'pytest', 'email': 'pyteset2@test.com'}

    # 1. Check GET method returns 401 UNAUTHORIZED
    assert client.get(info_url.format(uid=2)).status_code == 401
    assert client.get(info_url.format(uid=3), headers=auth.header(token)).status_code == 401

    # 2. Check PUT method returns 401 UNAUTHORIZED
    assert client.put(info_url.format(uid=2), json=new_info).status_code == 401
    assert client.put(info_url.format(uid=3), json=new_info, headers=auth.header(token)).status_code == 401

    # 3. Check DELETE method returns 401 UNAUTHORIZED
    assert client.delete(info_url.format(uid=2)).status_code == 401
    assert client.delete(info_url.format(uid=3), headers=auth.header(token)).status_code == 401


def test_get_user_info(client, auth):
    token = auth.login('mickey@mouse.com', 'squeak-squeak').json['access_token']
    response = client.get(info_url.format(uid=2), headers=auth.header(token))

    # 1. Check that the response status code is 200 OK
    assert response.status_code == 200

    # 2. Check that the response contains the expected fields
    assert set(response.json.keys()) == {'name', 'email', 'registered_on', 'is_subscribed'}

    # 3. Check that the response contains the expected data
    assert response.json['name'] == 'Mickey'
    assert response.json['email'] == 'mickey@mouse.com'
    assert response.json['registered_on'] == '2020-01-01T00:00:00'


@pytest.mark.parametrize(('new_info', 'status_code'), (
        ({'name': 'Donald Duck', 'email': 'donald@duck.com', 'password': 'quack-quack'}, 200),
        ({'name': 'Donald Duck New', 'password': 'quack-quack-quack'}, 200),
        ({'name': 'Donald Duck'}, 200),
        ({'email': 'donald2@duck.com'}, 200),
        ({'password': 'apple-orange-banana'}, 200),
        ({'email': 'minnie@mouse.com'}, 409),  # Email already exists
        ({'name': ''}, 422),  # Name is too short
        ({'name': 'x' * 40}, 422),  # Name is too long
        ({'email': 'xxxx'}, 422),  # Email is not valid
        ({'password': 'x' * 4}, 422),  # Password is too short
        ({'password': 'x' * 40}, 422),  # Password is too long
))
def test_update_user_info(client, auth, new_info, status_code):
    token = auth.login('donald@duck.com', 'quack-quack').json['access_token']
    response = client.put(info_url.format(uid=4), json=new_info, headers=auth.header(token))

    # 1. Check that the response status code is as expected
    assert response.status_code == status_code

    if status_code != 200:
        return

    # 2. Check the response contains the expected fields
    assert set(response.json.keys()) == {'name', 'email', 'registered_on', 'is_subscribed'}

    # 3. Check the response contains the expected data
    if 'name' in new_info:
        assert response.json['name'] == new_info['name']
    if 'email' in new_info:
        assert response.json['email'] == new_info['email']

    # 4. Check the password is updated
    if 'password' in new_info:
        assert auth.login(response.json['email'], new_info['password']).status_code == 201


@pytest.mark.parametrize('user_info', (
        {'uid': 4, 'email': 'donald@duck.com', 'password': 'quack-quack', 'sub_id': None},
        {'uid': 5, 'email': 'daisy@duck.com', 'password': 'quack-quack', 'sub_id': 3},
))
def test_delete_user(app, client, auth, user_info):
    token = auth.login(user_info['email'], user_info['password']).json['access_token']
    response = client.delete(info_url.format(uid=user_info['uid']), headers=auth.header(token))

    # 1. Check that the response status code is 204 NO CONTENT
    assert response.status_code == 204

    # 2. Check the user/(subscription) is moved to the recycled table
    with app.app_context():
        assert db.session.execute(
            db.select(UserModel).where(UserModel.uid == user_info['uid'])
        ).scalar_one_or_none() is None
        assert db.session.execute(
            db.select(UserRecycledModel).where(UserRecycledModel.uid == user_info['uid'])
        ).scalar_one_or_none() is not None
        if user_info['sub_id']:
            assert db.session.execute(
                db.select(SubscriptionRecycledModel).where(SubscriptionRecycledModel.sid == user_info['sub_id'])
            ).scalar_one_or_none() is not None

    # 3. Check the token is blacklisted
    assert auth.status(token).status_code == 401
