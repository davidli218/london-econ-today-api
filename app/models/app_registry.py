from typing import Optional

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.extensions import db


class AppRegistryModel(db.Model):
    __tablename__ = 'app_registry'

    key: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[Optional[str]]
