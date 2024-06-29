from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.extensions import db


class HousingModel(db.Model):
    __tablename__ = 'ds_housing'

    sid: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int]
    month: Mapped[int]
    value_ldn: Mapped[Optional[float]]
    annual_growth_ldn: Mapped[Optional[float]]
    value_uk: Mapped[Optional[float]]
    annual_growth_uk: Mapped[Optional[float]]


class TravelModel(db.Model):
    __tablename__ = 'ds_travel'

    sid: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int]
    period: Mapped[int]
    period_begin: Mapped[datetime]
    tube_journeys: Mapped[Optional[int]]
    bus_journeys: Mapped[Optional[int]]
    tube_journeys_avg: Mapped[Optional[int]]
    bus_journeys_avg: Mapped[Optional[int]]


class LabourMarketModel(db.Model):
    __tablename__ = 'ds_labour_market'

    sid: Mapped[int] = mapped_column(primary_key=True)
    quarter_mid_y: Mapped[int]
    quarter_mid_m: Mapped[int]
    unemployment_rate_ldn: Mapped[Optional[float]]
    unemployment_rate_uk: Mapped[Optional[float]]
