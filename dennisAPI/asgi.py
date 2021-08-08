"""
ASGI config for dennisAPI project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import django
django.setup()

from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import alpaca.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dennisAPI.settings')

# whenever connection is made to channels server, ProtocolTypeRouter will determine type ws:// or wss://

from rest_framework.request import Request
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication

def get_user_jwt(request):
    user = request.user
    # if user.is_authenticated():
    #     return user
    # try:
    #     user_jwt = JSONWebTokenAuthentication().authenticate(Request(request))
    #     if user_jwt is not None:
    #         return user_jwt[0]
    # except:
    #     pass
    return user

class AuthenticationMiddlewareJWT(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."

        request.user = SimpleLazyObject(lambda: get_user_jwt(request))

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": JWTAuthMiddlewareStack(
        URLRouter(
            alpaca.routing.websocket_urlpatterns
        )
    ),
})