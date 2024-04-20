from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    EpisodeViewSet,
    ChannelViewSet,
    PlayListViewSet,
    CommentViewSet,
    UserChannelViewSet,
)

router_episode = DefaultRouter()
router_channels = DefaultRouter()
router_play_list = DefaultRouter()
router_comment = DefaultRouter()
router_followers = DefaultRouter()
router_episode.register(r'', EpisodeViewSet)
router_channels.register(r'', ChannelViewSet)
router_play_list.register(r'', PlayListViewSet)
router_comment.register(r'', CommentViewSet)
router_followers.register(r'', UserChannelViewSet)

urlpatterns = [
    path('episode/', include(router_episode.urls)),
    path('channel/', include(router_channels.urls)),
    path('playlist/', include(router_play_list.urls)),
    path('comment/', include(router_comment.urls)),
    path('followers/', include(router_followers.urls)),

]
