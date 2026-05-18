import os
import requests
import logging

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self):
        self.api_key = os.environ.get('WEATHERAPI_KEY')
        self.base_url = 'https://api.weatherapi.com/v1/current.json'

    def get_weather(self, location: str = "Bengaluru"):
        """
        Fetches current weather.
        Uses a smart fallback to mock data if the API key is not present or if the request fails.
        """
        if not self.api_key:
            logger.warning("WEATHERAPI_KEY not found. Using simulated weather data.")
            return self._get_mock_weather()

        try:
            params = {
                'q': location,
                'key': self.api_key
            }
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            return {
                'condition': data['current']['condition']['text'],
                'temperature': data['current']['temp_c'],
                'wind_speed': data['current']['wind_kph'],
                'visibility': data['current']['vis_km'],
                'is_mock': False
            }
        except Exception as e:
            logger.warning(f"Weather API failed ({e}). Falling back to simulated weather data.")
            return self._get_mock_weather()

    def _get_mock_weather(self):
        """Generates realistic mock weather data for the simulation."""
        return {
            "condition": "Simulated Weather",
            "temperature": 28,
            "wind_speed": 10,
            "visibility": 8,
            "is_mock": True
        }

weather_service = WeatherService()
