from django.urls import re_path,path

from . import consumers

websocket_urlpatterns = [
    path(r'ws/mechanic/notifications/', consumers.MechanicNotificationConsumer.as_asgi()),
    path("ws/driver/notifications/",consumers.DriverNotificationConsumer.as_asgi()),
]