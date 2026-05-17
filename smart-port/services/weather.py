import os
import requests
import logging

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self):
        self.api_key = os.environ.get('OPENWEATHER_API_KEY')
        self.city = 'Rotterdam' # Default port city
        self.base_url = 'https://api.openweathermap.org/data/2.5/weather'

    def get_weather(self):
        """
        Fetches current weather.
        Uses a smart fallback to mock data if the API key is not present or if the request fails.
        """
        if not self.api_key:
            logger.info("OPENWEATHER_API_KEY not found. Using simulated weather data.")
            return self._get_mock_weather()

        try:
            params = {
                'q': self.city,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            return {
                'temperature': data['main']['temp'],
                'wind_speed': data['wind']['speed'],
                'condition': data['weather'][0]['main'],
                'risk_level': self._calculate_risk(data['wind']['speed'], data['weather'][0]['main'])
            }
        except Exception as e:
            logger.error(f"Weather API failed ({e}). Falling back to simulated weather data.")
            return self._get_mock_weather()

    def _get_mock_weather(self):
        """Generates realistic mock weather data for the simulation."""
        import random
        conditions = ['Clear', 'Clouds', 'Rain', 'Drizzle', 'Thunderstorm']
        condition = random.choice(conditions)
        wind_speed = random.uniform(2.0, 25.0)
        
        return {
            'temperature': random.uniform(10.0, 30.0),
            'wind_speed': round(wind_speed, 2),
            'condition': condition,
            'risk_level': self._calculate_risk(wind_speed, condition)
        }

    def _calculate_risk(self, wind_speed, condition):
        if wind_speed > 20.0 or condition == 'Thunderstorm':
            return 'High'
        elif wind_speed > 15.0 or condition == 'Rain':
            return 'Medium'
        return 'Low'

weather_service = WeatherService()
