from app.extensions import db
from app.models import SubscriptionModel
from app.models import SubscriptionRecycledModel

scp_url = '/api/v1/user/{uid}/subscription'


def test_user_subscription_privacy(client, auth):
    token = auth.login('pyteset@test.com', 'pytest-123456').json['access_token']

    # 1. Check POST method returns 401 UNAUTHORIZED
    assert client.post(scp_url.format(uid=2)).status_code == 401
    assert client.post(scp_url.format(uid=3), headers=auth.header(token)).status_code == 401

    # 2. Check DELETE method returns 401 UNAUTHORIZED
    assert client.delete(scp_url.format(uid=2)).status_code == 401
    assert client.delete(scp_url.format(uid=3), headers=auth.header(token)).status_code == 401


def test_create_user_subscription(app, client, auth):
    token = auth.login('minnie@mouse.com', 'squeak-squeak').json['access_token']

    # 1. Check the response status code is 201 CREATED
    assert client.post(scp_url.format(uid=3), headers=auth.header(token)).status_code == 201

    # 2. Check subscription is created in the database
    with app.app_context():
        assert db.session.execute(
            db.select(SubscriptionModel).where(SubscriptionModel.user_id == 3)
        ).scalar_one_or_none() is not None


def test_create_user_subscription_twice(client, auth):
    token = auth.login('mickey@mouse.com', 'squeak-squeak').json['access_token']

    # 1. Check the response status code is 409 CONFLICT
    assert client.post(scp_url.format(uid=2), headers=auth.header(token)).status_code == 409


def test_delete_user_subscription(app, client, auth):
    token = auth.login('daisy@duck.com', 'quack-quack').json['access_token']

    # 1. Check the response status code is 204 NO CONTENT
    assert client.delete(scp_url.format(uid=5), headers=auth.header(token)).status_code == 204

    # 2. Check subscription is moved to the recycle table
    with app.app_context():
        assert db.session.execute(
            db.select(SubscriptionModel).where(SubscriptionModel.user_id == 5)
        ).scalar_one_or_none() is None
        assert db.session.execute(
            db.select(SubscriptionRecycledModel).where(SubscriptionRecycledModel.sid == 3)
        ).scalar_one_or_none() is not None


def test_delete_user_subscription_twice(client, auth):
    token = auth.login('donald@duck.com', 'quack-quack').json['access_token']

    # 1. Check the response status code is 409 CONFLICT
    assert client.delete(scp_url.format(uid=4), headers=auth.header(token)).status_code == 409
