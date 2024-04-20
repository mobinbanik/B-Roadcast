from rest_framework import serializers
from podcasts.models import (
    Episode,
    Channel,
    PlayList,
    ItemInPlayList,
    Comment,
    UserChannel,
)


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
            'view_count',
            'like_count',
            'dislike_count',
        ]


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = [
            'title',
            'slug',
            'channel_id',
            'description',
            'session_count',
            'view_count',
            'subscribe_count',
            'creator',
            'thumbnail',
        ]


class PlayListSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayList
        fields = [
            'pk',
            'title',
            'created_at',
            'user',
            'index',
        ]


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'text',
            'comment_id',
            'created_at',
            'user',
            'episode',
            'like_count',
            'dislike_count',
            'episode',
            'is_reply',
            'reply_to',

        ]


class UserChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserChannel
        fields = [
            'user',
            'channel',

        ]

