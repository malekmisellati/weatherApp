import psycopg2
import json

conn = psycopg2.connect(
    dbname="weather_db",
    user="user",
    password="password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()


print("Retrieving sample embeddings from the database:")
cursor.execute("""
    SELECT name, longitude, latitude, name_embedding 
    FROM weather_locations 
    LIMIT 5;
""")
sample_records = cursor.fetchall()


for record in sample_records:
    name, longitude, latitude, embedding = record

    embedding_list = json.loads(embedding.replace("'", ""))  
    truncated_embedding = embedding_list[:5]  
    print(f"City: {name}")
    print(f"Longitude: {longitude}, Latitude: {latitude}")
    print(f"Embedding (first 5 values): {truncated_embedding}")
    print()

cursor.close()
conn.close()