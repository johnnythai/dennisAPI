from django.urls import re_path


from . import consumers

# as_asgi() insantiates instance of consumer for each connection, similar to as_view()
websocket_urlpatterns = [
    # re_path(r'ws/alpaca/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/alpaca/stream/', consumers.AlpacaConsumer.as_asgi())
]