import requests, json
from dotenv import load_dotenv
import os
import googlemaps

load_dotenv()

api_key = os.getenv("API_KEY")

gmaps = googlemaps.Client(key=api_key)

origin = "The Diamond, Sheffield, United Kingdom"
destination = "Hadfield Building, Sheffield, United Kingdom"

distance_result = gmaps.distance_matrix(origin, destination, mode='walking')

print(f"distance_result: {distance_result}")

distance = distance_result['rows'][0]['elements'][0]['distance']['text']
print(f"distance: {distance}")
duration = distance_result['rows'][0]['elements'][0]['duration']['text']
print(f"duration: {duration}")