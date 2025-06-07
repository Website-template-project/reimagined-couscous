"""
ASGI config for setup project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

# It's a good practice to import app-specific routing here.
# Make sure you have an 'api/routing.py' file (or for whichever app handles websockets)
# that defines 'websocket_urlpatterns'.
# Example:
# from api import routing as api_routing
import api.routing # Assuming 'api' is your app with WebSocket consumers and routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")

# Get the default Django ASGI application (for HTTP requests)
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator( # Apply security for WebSocket origins based on ALLOWED_HOSTS
            AuthMiddlewareStack(  # Handle authentication for WebSockets (uses Django's auth system)
                URLRouter(api.routing.websocket_urlpatterns) # Route WebSocket connections to your app's router
            )
        ),
    }
)
