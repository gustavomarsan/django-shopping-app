from django.apps import AppConfig
import asyncio


class ShopappConfig(AppConfig):
    name = 'shopapp'


    def ready(self):

        from .services.weather_service import weather_refresh_loop

        loop = asyncio.get_event_loop()

        loop.create_task(weather_refresh_loop())