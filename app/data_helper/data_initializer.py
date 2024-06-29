from pathlib import Path

import pandas as pd


class DataInitializer:
    prepared_data_path = Path(__file__).parent / 'local' / 'dataset_prepared.xlsx'

    def __init__(self, engine):
        self.__engine = engine
        self.__prepared_data = pd.read_excel(self.prepared_data_path, sheet_name=None, engine='openpyxl')

    def run(self):
        self._import_housing_data()
        self._import_travel_data()
        self._import_lm_data()

    def _import_housing_data(self):
        housing_data = self.__prepared_data['Housing']

        # Convert Month to datetime and extract Year and Month
        housing_period = pd.to_datetime(housing_data['Month']).dt.to_period("M")
        housing_data['Year'] = housing_period.dt.year
        housing_data['Month'] = housing_period.dt.month

        # Reorder and rename columns
        housing_data = housing_data[
            ['Year', 'Month', 'Value(LDN)', 'Annual_Growth(LDN)', 'Value(UK)', 'Annual_Growth(UK)']
        ]
        housing_data.columns = ['year', 'month', 'value_ldn', 'annual_growth_ldn', 'value_uk', 'annual_growth_uk']

        # Write to database
        housing_data.to_sql('ds_housing', self.__engine, if_exists='append', index=False)

    def _import_travel_data(self):
        travel_data = self.__prepared_data['Travel']

        # Extract Year and Period
        travel_data[['year', 'period']] = travel_data['Period'].str.extract(r'(\d{4})/(\d{4}) - (\d{1,2})')[[0, 2]]

        # Drop unnecessary columns
        travel_data.drop(columns=['Period'], inplace=True)
        travel_data.drop(columns=['Total_Journeys'], inplace=True)
        travel_data.drop(columns=['Total_Journeys(Moving_Average)'], inplace=True)

        # Reorder and rename columns
        travel_data = travel_data[[
            'year', 'period', 'Period_Begin', 'Tube_Journeys', 'Bus_Journeys',
            'Tube_Journeys(Moving_Average)', 'Bus_Journeys(Moving_Average)'
        ]]
        travel_data.columns = [
            'year', 'period', 'period_begin', 'tube_journeys', 'bus_journeys', 'tube_journeys_avg', 'bus_journeys_avg'
        ]

        # Write to database
        travel_data.to_sql('ds_travel', self.__engine, if_exists='append', index=False)

    def _import_lm_data(self):
        lm_data = self.__prepared_data['Labour Market']

        # Convert Month to datetime and extract Year and Month
        quarter_mid = pd.to_datetime(lm_data['Quarter_Mid']).dt.to_period("M")
        lm_data['quarter_mid_y'] = quarter_mid.dt.year
        lm_data['quarter_mid_m'] = quarter_mid.dt.month

        # Drop unnecessary columns
        lm_data.drop(columns=['Quarter_Mid'], inplace=True)

        # Reorder and rename columns
        lm_data = lm_data[
            ['quarter_mid_y', 'quarter_mid_m', 'Unemployment_Rates(LDN)', 'Unemployment_Rates(UK)']
        ]
        lm_data.columns = ['quarter_mid_y', 'quarter_mid_m', 'unemployment_rate_ldn', 'unemployment_rate_uk']

        # Write to database
        lm_data.to_sql('ds_labour_market', self.__engine, if_exists='append', index=False)
