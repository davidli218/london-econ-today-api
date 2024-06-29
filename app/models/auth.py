from datetime import datetime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.extensions import db


class TokenBlocklistModel(db.Model):
    __tablename__ = "token_blocklist"

    id: Mapped[int] = mapped_column(primary_key=True)
    jti: Mapped[str] = mapped_column(db.String(36), index=True)
    revoked_at: Mapped[datetime]
