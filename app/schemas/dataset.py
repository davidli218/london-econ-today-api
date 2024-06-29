import marshmallow as ma

from flask import url_for


class DataQueryBaseSchema(ma.Schema):
    year_lower = ma.fields.Integer(required=False)
    year_upper = ma.fields.Integer(required=False)

    @ma.validates_schema
    def validate_year(self, data, **kwargs):
        if 'year_lower' in data and 'year_upper' in data:
            if data['year_lower'] > data['year_upper']:
                raise ma.ValidationError('year_lower should <= year_upper')


class HousingDataQuerySchema(DataQueryBaseSchema):
    month = ma.fields.Integer(required=False, validate=lambda x: 1 <= x <= 12)


class TravelDataQuerySchema(DataQueryBaseSchema):
    period = ma.fields.Integer(required=False, validate=lambda x: 1 <= x <= 13)


class LabourMarketDataQuerySchema(DataQueryBaseSchema):
    month = ma.fields.Integer(required=False, validate=lambda x: 1 <= x <= 12)


class HousingDataBriefSchema(ma.Schema):
    year_month = ma.fields.Function(lambda obj: f'{obj.year}-{obj.month:02d}')
    uri = ma.fields.Function(lambda obj: url_for('dataset.housing_data', sid=obj.sid, _external=True))


class HousingDataSchema(ma.Schema):
    year = ma.fields.Integer()
    month = ma.fields.Integer()
    value_ldn = ma.fields.Float()
    annual_growth_ldn = ma.fields.Float()
    value_uk = ma.fields.Float()
    annual_growth_uk = ma.fields.Float()


class TravelDataBriefSchema(ma.Schema):
    year_period = ma.fields.Function(lambda obj: f'{obj.year}/{obj.period:02d}')
    uri = ma.fields.Function(lambda obj: url_for('dataset.travel_data', sid=obj.sid, _external=True))


class TravelDataSchema(ma.Schema):
    year = ma.fields.Integer()
    period = ma.fields.Integer()
    period_begin = ma.fields.Date(format='%Y-%m-%d')
    tube_journeys = ma.fields.Integer()
    bus_journeys = ma.fields.Integer()
    tube_journeys_avg = ma.fields.Integer()
    bus_journeys_avg = ma.fields.Integer()


class LabourMarketDataBriefSchema(ma.Schema):
    year_month = ma.fields.Function(lambda obj: f'{obj.quarter_mid_y}-{obj.quarter_mid_m:02d}')
    uri = ma.fields.Function(lambda obj: url_for('dataset.labour_market_data', sid=obj.sid, _external=True))


class LabourMarketDataSchema(ma.Schema):
    quarter_mid_y = ma.fields.Integer()
    quarter_mid_m = ma.fields.Integer()
    unemployment_rate_ldn = ma.fields.Float()
    unemployment_rate_uk = ma.fields.Float()
