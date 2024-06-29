from typing import Optional

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.extensions import db


class AppRegistryModel(db.Model):
    __tablename__ = 'app_registry'

    sid: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str]
    value: Mapped[Optional[str]]
