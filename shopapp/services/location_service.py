from django.core.cache import cache
import requests

def get_user_location():

    cached_location = cache.get("user_location")

    if cached_location:
        return cached_location

    try:
        response = requests.get("https://ipapi.co/json/", timeout=3)
        data = response.json()

        city = data.get("city")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if city and latitude and longitude:
            print("Location service success:", city, latitude, longitude)
            cache.set("user_location", data, 86400)  # cache for 24 hours
            return {
                "city": data.get("city"),
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude")
            }

    except Exception as e:
        print("Location service fallback:", e)

    # fallback location if data is none. 
    return {
        "city": "Zapopan",
        "latitude": 20.7236,
        "longitude": -103.3848
        }
    