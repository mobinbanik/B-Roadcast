from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    EpisodeViewSet,
    # TitleViewSet,
)

router_episode = DefaultRouter()
router_channels = DefaultRouter()
router_episode.register(r'', EpisodeViewSet)
# router_channels.register(r'', TitleViewSet)

urlpatterns = [
    path('episode/', include(router_episode.urls)),
    # path('channel/', include(router_channels.urls)),

]
