import requests
import json
from pprint import pprint as pp

def stop_finder(api_key, name, type="any"):
    base_url = "https://api.transport.nsw.gov.au/v1/tp"
    endpoint = "/stop_finder"

    params = {
        "outputFormat": "rapidJSON",
        "coordOutputFormat": "EPSG:4326",
        "name_sf": name, #? The Name to find
        "TfNSWSF": "true",
        "type_sf": type
    }

    headers = {
        "Authorization": f"apikey {api_key}"
    }

    try:
        response = requests.get(base_url + endpoint, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()

        return data

    except requests.exceptions.RequestException as e:
        pp(f"An error occurred: {e}")
    except json.JSONDecodeError:
        pp("Failed to decode JSON from the response.")

def clean_stop(data):
    locations = data['locations']
    for loc in locations:
        if loc['isBest']:
            try:
                if loc['isGlobalId']:
                    return loc['id']
            except KeyError:
                raise TypeError("Not global ID")
# Berowra RSL, Berowra