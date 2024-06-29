from datetime import datetime, timedelta

from app.extensions import db
from app.models import SubscriptionModel
from app.models import UserModel


def import_test_data():
    db.session.add(UserModel(
        uid=1, name='pytest', email='pyteset@test.com', password='pytest-123456',
        registered_on=datetime(2019, 1, 1, )
    ))
    db.session.add(UserModel(
        uid=2, name='Mickey', email='mickey@mouse.com', password='squeak-squeak',
        registered_on=datetime(2020, 1, 1, )
    ))
    db.session.add(UserModel(
        uid=3, name='Minnie', email='minnie@mouse.com', password='squeak-squeak',
        registered_on=datetime(2020, 1, 1, )
    ))
    db.session.add(UserModel(
        uid=4, name='Donald', email='donald@duck.com', password='quack-quack',
        registered_on=datetime.now() - timedelta(days=2)
    ))
    db.session.add(UserModel(
        uid=5, name='Daisy', email='daisy@duck.com', password='quack-quack',
        registered_on=datetime.now() - timedelta(days=2)
    ))

    db.session.add(SubscriptionModel(sid=1, start_date=datetime(2019, 1, 2), user_id=1))
    db.session.add(SubscriptionModel(sid=2, start_date=datetime.now(), user_id=2))
    db.session.add(SubscriptionModel(sid=3, start_date=datetime.now(), user_id=5))

    db.session.commit()
