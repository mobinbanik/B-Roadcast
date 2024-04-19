from django.shortcuts import render
from rest_framework import viewsets
from .serializer import (
    EpisodeSerializer,
    # TitleBlogPostSerializer,
    )
from podcasts.models import Episode
from django_filters.rest_framework import DjangoFilterBackend


class EpisodeViewSet(viewsets.ModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['channel', 'session']


# class TitleViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = TitleBlogPostSerializer