import json

import pandas as pd
import requests


def get_wind_data(params):
    api_base = "https://www.renewables.ninja/api/"
    session = requests.session()
    url = api_base + "data/wind"

    response = session.get(url, params=params)
    parsed_response = json.loads(response.text)
    return pd.read_json(json.dumps(parsed_response["data"]), orient="index").squeeze()


if __name__ == "__main__":
    parameters = {
        'lat': 34.125,
        'lon': 39.814,
        'date_from': '2019-01-01',
        'date_to': '2019-12-31',
        'capacity': 1.0,
        'height': 100,
        'turbine': 'Vestas V80 2000',
        'format': 'json'
    }
    data = get_wind_data(parameters)
