from datetime import datetime
from dateutil import parser
import pytz

import json, requests
from pprint import pprint as pp

def convert_to_local(utc_string):
    try:
        utc_dt = parser.isoparse(utc_string)
        local_dt = utc_dt.astimezone()

        return local_dt.strftime("%Y-%m-%d | %H:%M:%S")

    except ValueError as e:
        print(f"Error parsing the date string: {e}")
        return ""

def current_date():
    now = datetime.now()
    return now.strftime('%Y%m%d')

def current_time():
    now = datetime.now()
    return now.strftime('%H%M')

def get_trip(api_key, origin, destination):
    base_url = "https://api.transport.nsw.gov.au/v1/tp"
    endpoint = "/trip"
    
    params = {
        "outputFormat": "rapidJSON",
        "coordOutputFormat": "EPSG:4326",
        "depArrMacro": "dep", #? Departure after/arrival before itdDate and itdTime
        "type_origin": "any",
        "name_origin": origin, #? Central station. Find others using stop_finder
        "type_destination": "any",
        "name_destination": destination, #? Find others using stop_finder
        "itdDate": current_date(),
        "itdTime": current_time()
    }
    
    headers = {
        "Authorization": f"apikey {api_key}"
    }

    try:
        response = requests.get(base_url + endpoint, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # with open('data.json', 'w') as f:
        #     json.dump(data, f, indent=2)
        # print("Successfully saved the API output to data.json")
        
        return data


    except requests.exceptions.RequestException as e:
        pp(f"An error occurred: {e}")
    except json.JSONDecodeError:
        pp("Failed to decode JSON from the response.")


def clean_trip(data):
    journeys = data['journeys']
    l_journeys = []
    for journey in journeys:
        j = []
        for leg in journey['legs']:
            j.append(leg['origin']['disassembledName'])
            j.append(convert_to_local(leg['origin']['departureTimeEstimated']))
            j.append(leg['destination']['disassembledName'])
            j.append(convert_to_local(leg['destination']['arrivalTimeEstimated']))
            l_journeys.append(j)
    return l_journeys
