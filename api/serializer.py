from rest_framework import serializers
from podcasts.models import Episode


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = [
            'episode_id',
            'title',
            'description',
            'channel',
            'session',
            'audio_file',
            'thumbnail',
        ]


# class TitleBlogPostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ['id', 'title',]
