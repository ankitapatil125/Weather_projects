import requests
from .models import Location, WeatherData

def get_weather_data(location_name):
    api_key = "YOUR_MET_OFFICE_API_KEY"  # Replace with your Met Office API key
    url = f"https://api.metoffice.gov.uk/val/wxfcs/all/json/{location_name}?parameters=temperature,precipitation,windSpeed,humidity"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def store_weather_data(location_name):
    weather_data = get_weather_data(location_name)
    if weather_data:
        # Assuming the response contains 'temperature', 'humidity', 'windSpeed', 'precipitation'
        location, created = Location.objects.get_or_create(city=location_name.split(',')[0], country=location_name.split(',')[1])
        
        for record in weather_data.get('properties', {}).get('timeseries', []):
            WeatherData.objects.create(
                location=location,
                temperature=record.get('temperature'),
                humidity=record.get('humidity'),
                wind_speed=record.get('windSpeed'),
                weather_condition=record.get('weatherCondition'),
                rainfall=record.get('precipitation', None),
            )
