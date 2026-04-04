import ssl
import certifi
import aiohttp
import asyncio
from django.core.cache import cache
from .location_service import get_user_location

ssl_context = ssl.create_default_context(cafile=certifi.where())

http_session = None

WEATHER_CACHE_KEY = "current_weather"
CACHE_TTL = 600

async def get_http_session():
    global http_session

    if http_session is None:
        http_session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl_context)
        )

    return http_session


def get_weather_icon(code):

    mapping = {
        0: "☀️",
        1: "🌤",
        2: "⛅",
        3: "☁️",
        61: "🌧",
        71: "❄️"
    }

    return mapping.get(code, "🌤")

async def get_current_weather():

    cached_weather = cache.get(WEATHER_CACHE_KEY)

    if cached_weather:
            return cached_weather
    
    location = get_user_location()
    latitude = location["latitude"]
    longitude = location["longitude"]
    city = location["city"]

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current_weather=true"
    )

    try:
        session = await get_http_session()
        async with session.get(url) as response:
            data = await response.json()

            current = data.get("current_weather")

            if not current:
                raise ValueError("Weather API missing current_weather")

            temperature = data["current_weather"]["temperature"]
            icon = get_weather_icon(data["current_weather"]["weathercode"])

            weather = {
                "city": city,
                "temperature": temperature,
                "icon": icon
            }
            # store for 10 minutes (600 seconds)
            cache.set(WEATHER_CACHE_KEY, weather, CACHE_TTL)

            return weather

    except Exception as e:
        print("Weather service fallback:", e)
        return {
            "city": city,
            "temperature": None,
            "icon": "🌤", 
        }
    


async def weather_refresh_loop():

    while True:
        try:
            print("Refreshing weather cache...")

            weather = await get_current_weather()

            print("Weather refreshed:", weather)

        except Exception as e:
            print("Weather refresh error:", e)

        # wait 10 minutes
        await asyncio.sleep(600)