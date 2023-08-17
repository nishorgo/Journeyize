from django.conf import settings

import requests
import time
import datetime


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


def fetch_weather_info(region_name, start_date, end_date):
    date = []
    avgtemp = []
    avg_humidity = []
    rain_probability = []
    snow_probability = []
    sunrise = []
    sunset = []
    
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    start_date_difference = (start_date - datetime.date.today()).days
    end_date_difference = (end_date - datetime.date.today()).days
    end_date_difference += 1
    
    api_url = "https://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": settings.WEATHER_API_KEY,
        "q": region_name,
        "days": 10,
        "aqi": "no",
        "alerts": "yes"
    }
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        daily_forecast = weather_data['forecast']['forecastday']
        for forecast in daily_forecast:
            date.append(forecast['date'])
            avgtemp.append(forecast['day']['avgtemp_c'])
            avg_humidity.append(forecast['day']['avghumidity'])
            rain_probability.append(forecast['day']['daily_chance_of_rain'])
            snow_probability.append(forecast['day']['daily_chance_of_snow'])
            sunrise.append(forecast['astro']['sunrise'])
            sunset.append(forecast['astro']['sunset'])

        return date[start_date_difference:end_date_difference], avgtemp[start_date_difference:end_date_difference], \
                avg_humidity[start_date_difference:end_date_difference], rain_probability[start_date_difference:end_date_difference], \
                snow_probability[start_date_difference:end_date_difference], sunrise[start_date_difference:end_date_difference], \
                sunset[start_date_difference:end_date_difference]
        
    else:
        return response.status_code
    
