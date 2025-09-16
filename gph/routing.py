from django.urls import re_path
from puzzles.messaging import TeamNotificationsConsumer, HintsConsumer

websocket_urlpatterns = [
    # 맨 앞에 /가 있어도 되고 없어도 되도록 ^/? 패턴을 사용합니다.
    re_path(r'^/?ws/team/?$', TeamNotificationsConsumer.as_asgi()),
    re_path(r'^/?ws/hints/?$', HintsConsumer.as_asgi()),
]