import requests
import json
from typing import Dict, List

class PlacesAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://google-map-places-new-v2.p.rapidapi.com/v1/places:autocomplete"
        self.headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "google-map-places-new-v2.p.rapidapi.com",
            "Content-Type": "application/json",
            "X-Goog-FieldMask": "*"
        }

    def search_places(self, query: str, lat: float, lon: float, radius: int = 10000) -> List[Dict]:
        payload = {
            "input": query,
            "locationBias": {
                "circle": {
                    "center": {
                        "latitude": lat,
                        "longitude": lon
                    },
                    "radius": radius
                }
            },
            "includeQueryPredictions": True
        }

        try:
            response = requests.post(self.base_url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json().get('places', [])
        except Exception as e:
            print(f"Error fetching places: {e}")
            return []

    def get_attractions(self, city: str, interests: List[str]) -> Dict[str, List[Dict]]:
        # Hardcoded coordinates for demo - in production, you'd want to geocode the city name
        sample_coordinates = {
            "New York": (40.7128, -74.0060),
            "London": (51.5074, -0.1278),
            "Tokyo": (35.6762, 139.6503),
            "Paris": (48.8566, 2.3522),
            # Add more cities as needed
        }

        lat, lon = sample_coordinates.get(city, (0, 0))
        attractions = {}

        for interest in interests:
            query = f"{interest} in {city}"
            places = self.search_places(query, lat, lon)
            attractions[interest] = places[:5]  # Get top 5 results for each interest

        return attractions 