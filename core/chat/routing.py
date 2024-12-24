from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/socket-server/<int:room>', ChatConsumer.as_asgi())
]