import requests
import json
import pandas as pd
import psycopg2
from sentence_transformers import SentenceTransformer
from psycopg2.extras import execute_batch


api_key = '' #Insert Api key here before running 
cities = ['Ottawa,Canada', 'Toronto,Canada', 'Vancouver,Canada', 'Montreal,Canada', 'Calgary,Canada']
weather_array = []


model = SentenceTransformer('all-MiniLM-L6-v2')  

for city in cities:
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city_name = data['location']['name']
        
        embedding = model.encode(city_name).tolist()  
        weather_info = {
            "name": city_name,
            "longitude": data['location']['lon'],
            "latitude": data['location']['lat'],
            "name_embedding": embedding
        }
        weather_array.append(weather_info)
    else:
        weather_array.append({"name": city.split(',')[0], "longitude": None, "latitude": None, "name_embedding": None})


print("Individual JSON responses:")
for weather in weather_array:
    print(json.dumps(weather, indent=2))
    print()


df = pd.DataFrame(weather_array)
print("Pandas DataFrame:")
print(df)


conn = psycopg2.connect(
    dbname="weather_db",
    user="user",
    password="password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_locations (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        longitude FLOAT,
        latitude FLOAT,
        name_embedding VECTOR(384)
    );
""")


batch_size = 100
print(f"Inserting data into PostgreSQL in batches of {batch_size}...")


data_to_insert = [
    (weather['name'], weather['longitude'], weather['latitude'], str(weather['name_embedding']))
    for weather in weather_array
]


for i in range(0, len(data_to_insert), batch_size):
    batch = data_to_insert[i:i + batch_size]
    execute_batch(
        cursor,
        """
        INSERT INTO weather_locations (name, longitude, latitude, name_embedding)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING;  -- Avoid duplicates if running multiple times
        """,
        batch
    )
    print(f"Inserted batch {i // batch_size + 1} ({len(batch)} records)")

conn.commit()
print("Data with embeddings inserted into PostgreSQL")


print("\nRetrieving sample embeddings from the database:")
cursor.execute("""
    SELECT name, longitude, latitude, name_embedding 
    FROM weather_locations 
    LIMIT 3;
""")
sample_records = cursor.fetchall()

for record in sample_records:
    name, lon, lat, embedding = record
    
    truncated_embedding = json.loads(embedding.replace("'", ""))[:5]  # Convert string to list and truncate
    print(f"City: {name}")
    print(f"Longitude: {lon}, Latitude: {lat}")
    print(f"Embedding (first 5 values): {truncated_embedding}")
    print()


cursor.close()
conn.close()