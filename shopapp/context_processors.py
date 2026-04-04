from asgiref.sync import async_to_sync
from .services.weather_service import get_current_weather

def weather_context(request):

    weather = async_to_sync(get_current_weather)()

    return {
        "weather": weather
    }