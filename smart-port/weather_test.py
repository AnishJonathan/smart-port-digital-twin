import os
import requests

# 1. Hardcode your key just for this quick local test
API_KEY = "4e7c491ad8c5473584042531261805"  
LOCATION = "Karlskrona"  # Or your preferred port city

url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={LOCATION}"

try:
    print("Sending request to WeatherAPI...")
    response = requests.get(url, timeout=5)
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ SUCCESS! Your API key is working locally.")
        print(f"Location: {data['location']['name']}, {data['location']['country']}")
        print(f"Condition: {data['current']['condition']['text']}")
        print(f"Wind Speed: {data['current']['wind_kph']} kph")
    else:
        print(f"\n❌ FAILED with Status Code: {response.status_code}")
        print(f"Response Error: {response.text}")

except Exception as e:
    print(f"\n❌ Connection Error: {e}")
