from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r'ws/<int:id>/', consumers.ChatConsumer.as_asgi()),
]