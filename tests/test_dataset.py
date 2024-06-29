import pytest

from app.extensions import db
from app.models import HousingModel
from app.models import LabourMarketModel
from app.models import TravelModel

housing_list_url = '/api/v1/dataset/housing'
housing_detail_url = '/api/v1/dataset/housing/{sid}'
travel_list_url = '/api/v1/dataset/travel'
travel_detail_url = '/api/v1/dataset/travel/{sid}'
labour_market_list_url = '/api/v1/dataset/labour-market'
labour_market_detail_url = '/api/v1/dataset/labour-market/{sid}'

generic_data_list_query_test_params = (
    ({}, 200),
    ({'year_lower': '2010', 'year_upper': '2020', 'month': '1'}, 200),
    ({'year_lower': '2015'}, 200),
    ({'year_upper': '2015'}, 200),
    ({'year_between': '2010'}, 200),  # invalid parameter should be ignored
    ({'year_lower': '2020', 'year_upper': '2010'}, 422),  # lower > upper should return 422
    ({'year_lower': 'xxxx', 'year_upper': 'yyyy'}, 422),  # invalid year should return 422
)


@pytest.mark.parametrize(('params', 'status_code'), (
        *generic_data_list_query_test_params,
        ({'month': '8'}, 200),
        ({'month': '13'}, 422),  # invalid month should return 422
))
def test_get_housing_list(app, client, params, status_code):
    response = client.get(housing_list_url, query_string=params)

    with app.app_context():
        query = db.select(HousingModel)
        if 'year_lower' in params:
            query = query.where(HousingModel.year >= params['year_lower'])
        if 'year_upper' in params:
            query = query.where(HousingModel.year <= params['year_upper'])
        if 'month' in params:
            query = query.where(HousingModel.month == params['month'])
        expected_datas = db.session.execute(query).scalars().all()

    # 1. Check that the response status code is 200 OK
    assert response.status_code == status_code

    if status_code != 200:
        return

    # 2. Check that the response contains the expected number of records
    assert len(response.json) == len(expected_datas)

    # 3. Check that the response contains the expected fields
    for housing_data in response.json:
        assert set(housing_data.keys()) == {'year_month', 'uri'}

    # 4. Check that the response.uri is valid
    for housing_data in response.json:
        assert client.get(housing_data['uri']).status_code == 200


def test_get_housing_detail(app, client):
    with app.app_context():
        housing_dataset = db.session.execute(db.select(HousingModel)).scalars().all()

    for housing_data in housing_dataset:
        response = client.get(housing_detail_url.format(sid=housing_data.sid))

        # 1. Check that the response status code is 200 OK
        assert response.status_code == 200

        # 2. Check that the response contains the expected fields
        expected_fields = {'year', 'month', 'value_ldn', 'annual_growth_ldn', 'value_uk', 'annual_growth_uk'}
        assert set(response.json.keys()) == expected_fields

        # 3. Check that the response contains the expected values
        assert response.json['year'] == housing_data.year
        assert response.json['month'] == housing_data.month
        assert response.json['value_ldn'] == housing_data.value_ldn
        assert response.json['annual_growth_ldn'] == housing_data.annual_growth_ldn
        assert response.json['value_uk'] == housing_data.value_uk
        assert response.json['annual_growth_uk'] == housing_data.annual_growth_uk

    # 4. Check that the invalid requests return 404 NOT FOUND
    assert client.get(housing_detail_url.format(sid=0)).status_code == 404
    assert client.get(housing_detail_url.format(sid=len(housing_dataset) + 1)).status_code == 404
    assert client.get(housing_detail_url.format(sid='xxx')).status_code == 404


@pytest.mark.parametrize(('params', 'status_code'), (
        *generic_data_list_query_test_params,
        ({'period': '8'}, 200),
        ({'period': '14'}, 422),  # invalid month should return 422
))
def test_get_travel_list(app, client, params, status_code):
    response = client.get(travel_list_url, query_string=params)

    with app.app_context():
        query = db.select(TravelModel)
        if 'year_lower' in params:
            query = query.where(TravelModel.year >= params['year_lower'])
        if 'year_upper' in params:
            query = query.where(TravelModel.year <= params['year_upper'])
        if 'period' in params:
            query = query.where(TravelModel.period == params['period'])
        expected_datas = db.session.execute(query).scalars().all()

    # 1. Check that the response status code is 200 OK
    assert response.status_code == status_code

    if status_code != 200:
        return

    # 2. Check that the response contains the expected number of records
    assert len(response.json) == len(expected_datas)

    # 3. Check that the response contains the expected fields
    for travel_data in response.json:
        assert set(travel_data.keys()) == {'year_period', 'uri'}

    # 4. Check that the response.uri is valid
    for travel_data in response.json:
        assert client.get(travel_data['uri']).status_code == 200


def test_get_travel_detail(app, client):
    with app.app_context():
        travel_dataset = db.session.execute(db.select(TravelModel)).scalars().all()

    for travel_data in travel_dataset:
        response = client.get(travel_detail_url.format(sid=travel_data.sid))

        # 1. Check that the response status code is 200 OK
        assert response.status_code == 200

        # 2. Check that the response contains the expected fields
        expected_fields = {
            'year', 'period', 'period_begin',
            'tube_journeys', 'bus_journeys', 'tube_journeys_avg', 'bus_journeys_avg'
        }
        assert set(response.json.keys()) == expected_fields

        # 3. Check that the response contains the expected values
        assert response.json['year'] == travel_data.year
        assert response.json['period'] == travel_data.period
        assert response.json['period_begin'] == travel_data.period_begin.strftime('%Y-%m-%d')
        assert response.json['tube_journeys'] == travel_data.tube_journeys
        assert response.json['bus_journeys'] == travel_data.bus_journeys
        assert response.json['tube_journeys_avg'] == travel_data.tube_journeys_avg
        assert response.json['bus_journeys_avg'] == travel_data.bus_journeys_avg

    # 4. Check that the invalid requests return 404 NOT FOUND
    assert client.get(travel_detail_url.format(sid=0)).status_code == 404
    assert client.get(travel_detail_url.format(sid=len(travel_dataset) + 1)).status_code == 404
    assert client.get(travel_detail_url.format(sid='xxx')).status_code == 404


@pytest.mark.parametrize(('params', 'status_code'), (
        *generic_data_list_query_test_params,
        ({'month': '8'}, 200),
        ({'month': '13'}, 422),  # invalid month should return 422
))
def test_get_labour_market_list(app, client, params, status_code):
    response = client.get(labour_market_list_url, query_string=params)

    with app.app_context():
        query = db.select(LabourMarketModel)
        if 'year_lower' in params:
            query = query.where(LabourMarketModel.quarter_mid_y >= params['year_lower'])
        if 'year_upper' in params:
            query = query.where(LabourMarketModel.quarter_mid_y <= params['year_upper'])
        if 'month' in params:
            query = query.where(LabourMarketModel.quarter_mid_m == params['month'])
        expected_datas = db.session.execute(query).scalars().all()

    # 1. Check that the response status code is 200 OK
    assert response.status_code == status_code

    if status_code != 200:
        return

    # 2. Check that the response contains the expected number of records
    assert len(response.json) == len(expected_datas)

    # 3. Check that the response contains the expected fields
    for labour_market_data in response.json:
        assert set(labour_market_data.keys()) == {'year_month', 'uri'}

    # 4. Check that the response.uri is valid
    for labour_market_data in response.json:
        assert client.get(labour_market_data['uri']).status_code == 200


def test_get_labour_market_detail(app, client):
    with app.app_context():
        labour_market_dataset = db.session.execute(db.select(LabourMarketModel)).scalars().all()

    for labour_market_data in labour_market_dataset:
        response = client.get(labour_market_detail_url.format(sid=labour_market_data.sid))

        # 1. Check that the response status code is 200 OK
        assert response.status_code == 200

        # 2. Check that the response contains the expected fields
        expected_fields = {
            'quarter_mid_y', 'quarter_mid_m', 'unemployment_rate_ldn', 'unemployment_rate_uk'
        }
        assert set(response.json.keys()) == expected_fields

        # 3. Check that the response contains the expected values
        assert response.json['quarter_mid_y'] == labour_market_data.quarter_mid_y
        assert response.json['quarter_mid_m'] == labour_market_data.quarter_mid_m
        assert response.json['unemployment_rate_ldn'] == labour_market_data.unemployment_rate_ldn
        assert response.json['unemployment_rate_uk'] == labour_market_data.unemployment_rate_uk

    # 4. Check that the invalid requests return 404 NOT FOUND
    assert client.get(labour_market_detail_url.format(sid=0)).status_code == 404
    assert client.get(labour_market_detail_url.format(sid=len(labour_market_dataset) + 1)).status_code == 404
    assert client.get(labour_market_detail_url.format(sid='xxx')).status_code == 404
