import requests
import json
import pandas as pd


api_key = '' #Insert Api key here before running
cities = ['Ottawa,Canada', 'Toronto,Canada', 'Vancouver,Canada', 'Montreal,Canada', 'Calgary,Canada']


weather_array = []

for city in cities:
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        weather_info = {
            "name": data['location']['name'],
            "longitude": data['location']['lon'],
            "latitude": data['location']['lat']
        }
        weather_array.append(weather_info)
    else:
        weather_array.append({"name": city.split(',')[0], "longitude": None, "latitude": None})


print("Individual JSON responses:")
for weather in weather_array:
    print(json.dumps(weather, indent=2))
    print()


df = pd.DataFrame(weather_array)


print("Pandas DataFrame:")
print(df)