from django.conf import settings

import re
import requests
import time
import datetime

import openai


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


def fetch_weather_information(region_name, start_date, end_date):
    date = []
    avgtemp = []
    avg_humidity = []
    rain_probability = []
    snow_probability = []
    
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

        return date[start_date_difference:end_date_difference], avgtemp[start_date_difference:end_date_difference], \
                avg_humidity[start_date_difference:end_date_difference], rain_probability[start_date_difference:end_date_difference], \
                snow_probability[start_date_difference:end_date_difference]
        
    else:
        return response.status_code
    

def generate_traditional_foods(region_name):
    openai.api_key = settings.OPENAI_API_KEY
    
    prompt = (
        "You are a food and ethnicity expert. I am giving you a region name. You'll tell me about all the traditional and ethnic foods of that region.\n\n" 

        "Step 1: Generate a numbered list of all the traditional and ethnic foods from that region.\n"
        "Step 2: Give a brief about each of the foods.\n\n"
        
        f"Region name: {region_name}"
    )

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3000
    )

    foods = response.choices[0].text.strip()

    pattern = r'(\d+)\. ([^:]+): (.+)'
    matches = re.findall(pattern, foods)

    food_dictionary = {}

    for match in matches:
        name = match[1]
        description = match[2]
        food_dictionary[name] = description

    return food_dictionary


def generate_itinerary(region_name, dates, selected_places, duration, avgtemp=None, avg_humidity=None, rain_probability=None, snow_probability=None):
    openai.api_key = settings.OPENAI_API_KEY

    prompt_with_weather = (
        "Suppose, you are a travel expert. Based on the places listed below, I'm seeking your expert assistance in curating a perfect itinerary for the following weather. "
        "Suggest a range of activities in the places listed below that would align with this weather condition? Feel free to propose recreational activities, and local gems. "
        "It would be immensely helpful if you could provide estimated durations for each activity, as well as any valuable tips or insights. I repeat, focus on the places listed below only.\n\n"

        f"Destination = {region_name}\n" 
        f"places = {selected_places}\n" 
        f"dates = {dates}" 
        f"temperature in celcius = {avgtemp}"
        f"average humidity in percentage= {avg_humidity}"
        f"probability of rain in percentage= {rain_probability}" 
        f"probability of snow in percentage= {snow_probability}" 
        f"Duration of the tour: {duration} days\n\n"

        "Follow the steps:"
        "Step 1: Make lists of indoor, outdoor and recreational activities on those places." 
        "Step 2: If the probability of rain or snow in percentage is more than 60, then prioritize on the indoor items while making the itinerary."
        "Step 3: Output the itinerary activities formatted in separated by days."
    )

    prompt_without_weather = (
        "Suppose, you are a travel expert. I'm seeking your expert assistance in curating a perfect itinerary for the places listed below. "
        "Suggest a range of activities in the places listed below. Feel free to propose recreational activities, and local gems. "
        "It would be immensely helpful if you could provide estimated durations for each activity, as well as any valuable tips or insights. I repeat, focus on the places listed below only.\n\n"

        f"Destination = {region_name}\n" 
        f"places = {selected_places}\n"
        f"Duration of the tour: {duration} days\n\n"

        "Follow the steps:"
        "Step 1: Make lists of indoor, outdoor and recreational activities on those places." 
        "Step 2: Output the itinerary activities formatted in separated by days."
    )

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt_with_weather if avgtemp else prompt_without_weather,
        max_tokens=3000
    )

    itinerary_whole = response.choices[0].text.strip()
    pattern = r'Day \d+:?'
    itinerary_list = re.split(pattern, itinerary_whole)
    itinerary_list = [itinerary.strip() for itinerary in itinerary_list if itinerary.strip()]

    return itinerary_list