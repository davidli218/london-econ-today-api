from datetime import datetime
from typing import TYPE_CHECKING

from argon2.exceptions import VerifyMismatchError  # noqa
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.extensions import db, ph

if TYPE_CHECKING:
    from app.models import SubscriptionModel


class UserModel(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'sqlite_autoincrement': True}

    uid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    _password: Mapped[str]
    registered_on: Mapped[datetime] = mapped_column(default=db.func.now())

    subscription: Mapped['SubscriptionModel'] = db.relationship(back_populates='user')

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext_password):
        self._password = ph.hash(plaintext_password)  # noqa

    def verify_password(self, plaintext_password):
        try:
            return ph.verify(self.password, plaintext_password)
        except VerifyMismatchError:
            return False

    def is_password_weak(self):
        return ph.check_needs_rehash(self.password)

    def to_recycled(self) -> 'UserRecycledModel':
        return UserRecycledModel(
            uid=self.uid,
            name=self.name,
            email=self.email,
            password=self.password,
            registered_on=self.registered_on,
            recycled_on=db.func.now()
        )


class UserRecycledModel(db.Model):
    __tablename__ = 'recycled_user'

    uid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    registered_on: Mapped[datetime]
    recycled_on: Mapped[datetime]
