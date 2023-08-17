from django.conf import settings

import requests
import time
from datetime import datetime, timedelta


today_date = datetime.now()
print(today_date + timedelta(days=10))

def fetch_tourist_attractions(region_name):
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    attractions = []
    next_page_token = None
    
    while True:
        if len(attractions) == 100: break
        params = {
            "query": f"Tourist attractions in {region_name} ",
            "radius": 50000,
            'rankby': 'prominence',
            "key": settings.GOOGLE_MAPS_API_KEY
        }
        
        if next_page_token:
            params["pagetoken"] = next_page_token
        
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if data.get("results"):
            attractions.extend(data["results"])
        
        next_page_token = data.get("next_page_token")
        if not next_page_token:
            break

        time.sleep(2)
    
    return attractions