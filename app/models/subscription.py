from datetime import datetime
from typing import Optional
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.extensions import db

if TYPE_CHECKING:
    from app.models.user import UserModel


class SubscriptionModel(db.Model):
    __tablename__ = 'subscription'
    __table_args__ = {'sqlite_autoincrement': True}

    sid: Mapped[int] = mapped_column(primary_key=True)
    start_date: Mapped[datetime] = mapped_column(default=db.func.now())
    last_sent: Mapped[Optional[datetime]]
    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.uid'))

    user: Mapped['UserModel'] = db.relationship(back_populates='subscription')

    def to_recycled(self) -> 'SubscriptionRecycledModel':
        return SubscriptionRecycledModel(
            sid=self.sid,
            start_date=self.start_date,
            end_date=db.func.now(),
            last_sent=self.last_sent,
            user_id=self.user_id
        )


class SubscriptionRecycledModel(db.Model):
    __tablename__ = 'recycled_subscription'

    sid: Mapped[int] = mapped_column(primary_key=True)
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]
    last_sent: Mapped[Optional[datetime]]
    user_id: Mapped[int]
