from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .serializer import (
    EpisodeSerializer,
    ChannelSerializer,
    PlayListSerializer,
    CommentSerializer,
    UserChannelSerializer,
    UserSerializer,
    UserDislikeSerializer,
    UserLikeSerializer,
    )
from podcasts.models import (
    Episode,
    Channel,
    PlayList,
    ItemInPlayList,
    User,
    UserLike,
    UserDislike,
    Comment,
    UserChannel,
)
from django_filters.rest_framework import DjangoFilterBackend


"""
    @action(detail=True, ...
    detail : if you want to do an action for 1 object : True
             if you want to do an action for all objects : False
             
    DefaultRouter add <pk> of an object to url if detail=True.
"""


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'user',
        'comment_id',
        'episode',
        'is_active',
        'is_reply',
        'reply_to',
    ]

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        username = request.user.username
        user = get_object_or_404(User, username=username)
        comment = get_object_or_404(Comment, pk=pk)
        user_like, created = UserLike.objects.get_or_create(comment=comment, user=user)
        if created:
            comment.like_count += 1
            comment.save()
            return Response({'status': 'Done!', 'likes': comment.like_count})
        else:
            return Response({'status': 'you already liked this comment.',  'likes': comment.like_count})

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def dislike(self, request, pk=None):
        username = request.user.username
        user = get_object_or_404(User, username=username)
        comment = get_object_or_404(Comment, pk=pk)
        user_like, created = UserDislike.objects.get_or_create(comment=comment, user=user)
        if created:
            comment.dislike_count += 1
            comment.save()
            return Response({'status': 'Done!', 'dislikes': comment.dislike_count})
        else:
            return Response({'status': 'you already disliked this comment.', 'dislikes': comment.dislike_count})

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def rmlike(self, request, pk=None):
        username = request.user.username
        user = get_object_or_404(User, username=username)
        comment = get_object_or_404(Comment, pk=pk)
        try:
            user_like = UserLike.objects.get(comment=comment, user=user)
        except UserLike.DoesNotExist:
            return Response({'status': "you didn't liked this comment yet.", 'likes': comment.like_count})
        else:
            comment.like_count -= 1
            comment.save()
            user_like.delete()
            return Response({'status': 'removed!', 'likes': comment.like_count})

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def rmdislike(self, request, pk=None):
        username = request.user.username
        user = get_object_or_404(User, username=username)
        comment = get_object_or_404(Comment, pk=pk)
        try:
            user_dislike = UserDislike.objects.get(comment=comment, user=user)
        except UserDislike.DoesNotExist:
            return Response({'status': "you didn't disliked this comment yet.", 'dislikes': comment.dislike_count})
        else:
            comment.dislike_count -= 1
            comment.save()
            user_dislike.delete()
            return Response({'status': 'removed!', 'disliked': comment.dislike_count})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def replay(self, request, pk=None):
        username = request.user.username
        user = get_object_or_404(User, username=username)
        try:
            comment = get_object_or_404(Comment, pk=pk)
        except Comment.DoesNotExist:
            return Response({'status': "This comment does not exist."})
        else:
            episode = comment.episode
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                Comment.objects.create(
                    user=user,
                    episode=episode,
                    text=serializer.validated_data['text'],
                    is_replay=True,
                    reply_to=comment,
                )
                return Response({'status': 'Done!'})
            else:
                return Response(serializer.errors)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def comment(self, request, pk=None):
        username = request.user.username
        user = get_object_or_404(User, username=username)
        episode = get_object_or_404(Episode, pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            Comment.objects.create(
                user=user,
                episode=episode,
                text=serializer.validated_data['text'],
                is_replay=False,
            )
            return Response({'status': 'Done!'})
        else:
            return Response(serializer.errors)

    @action(detail=True, methods=['post', 'get', 'delete'], permission_classes=[IsAuthenticated])
    def id(self, request, pk=None):
        comment = get_object_or_404(Episode, pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment.text = serializer.validated_data['text']
            comment.is_active = serializer.validated_data['is_active']
            comment.save()
            return Response({'status': 'Done!'})
        else:
            return Response(serializer.errors)


class EpisodeViewSet(viewsets.ModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['channel', 'session', 'episode_id']

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        username = request.user.username
        user = get_object_or_404(User, username=username)
        episode = get_object_or_404(Episode, pk=pk)
        user_like, created = UserLike.objects.get_or_create(episode=episode, user=user)
        if created:
            episode.like_count += 1
            episode.save()
            return Response({'status': 'Done!', 'likes': episode.like_count})
        else:
            return Response({'status': 'you already liked this episode.',  'likes': episode.like_count})

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def dislike(self, request, pk=None):
        username = request.user.username
        user = get_object_or_404(User, username=username)
        episode = get_object_or_404(Episode, pk=pk)
        user_like, created = UserDislike.objects.get_or_create(episode=episode, user=user)
        if created:
            episode.dislike_count += 1
            episode.save()
            return Response({'status': 'Done!', 'dislikes': episode.dislike_count})
        else:
            return Response({'status': 'you already disliked this episode.', 'dislikes': episode.dislike_count})

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def rmlike(self, request, pk=None):
        username = request.user.username
        user = get_object_or_404(User, username=username)
        episode = get_object_or_404(Episode, pk=pk)
        try:
            user_like = UserLike.objects.get(episode=episode, user=user)
        except UserLike.DoesNotExist:
            return Response({'status': "you didn't liked this episode yet.", 'likes': episode.like_count})
        else:
            episode.like_count -= 1
            episode.save()
            user_like.delete()
            return Response({'status': 'removed!', 'likes': episode.like_count})

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def rmdislike(self, request, pk=None):
        username = request.user.username
        user = get_object_or_404(User, username=username)
        episode = get_object_or_404(Episode, pk=pk)
        try:
            user_dislike = UserDislike.objects.get(episode=episode, user=user)
        except UserDislike.DoesNotExist:
            return Response({'status': "you didn't disliked this episode yet.", 'dislikes': episode.dislike_count})
        else:
            episode.dislike_count -= 1
            episode.save()
            user_dislike.delete()
            return Response({'status': 'removed!', 'disliked': episode.dislike_count})

    @action(detail=True, methods=['post', 'get', 'delete'], permission_classes=[IsAuthenticated])
    def id(self, request, pk=None):
        episode = get_object_or_404(Episode, pk=pk)
        serializer = EpisodeSerializer(data=request.data)
        if serializer.is_valid():
            episode.title = serializer.validated_data['title']
            episode.description = serializer.validated_data['description']
            episode.channel = serializer.validated_data['channel']
            episode.session = serializer.validated_data['session']
            episode.audio_file = serializer.validated_data['audio_file']
            episode.thumbnail = serializer.validated_data['thumbnail']
            episode.save()
            return Response({'status': 'Done!'})
        else:
            return Response(serializer.errors)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):
        episode = get_object_or_404(Episode, pk=pk)
        comments = Comment.objects.all().filter(episode=episode)
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'user_id',
        'location',
        'username',
        'email',

    ]


class UserLikeViewSet(viewsets.ModelViewSet):
    queryset = UserLike.objects.all()
    serializer_class = UserLikeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'user',
        'episode',
        'comment',

    ]


class UserDislikeViewSet(viewsets.ModelViewSet):
    queryset = UserDislike.objects.all()
    serializer_class = UserDislikeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'user',
        'episode',
        'comment',

    ]


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug', 'channel_id', 'creator']


class UserChannelViewSet(viewsets.ModelViewSet):
    queryset = UserChannel.objects.all()
    serializer_class = UserChannelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'channel',]


class PlayListViewSet(viewsets.ModelViewSet):
    queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, permission_classes=[IsAuthenticated])
    def mylist(self, request):
        if request.user.is_superuser:
            play_lists = PlayList.objects.all()
        else:
            username = request.user.username
            user = get_object_or_404(User, username=username)
            play_lists = PlayList.objects.all().filter(user=user)

        page = self.paginate_queryset(play_lists)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(play_lists, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'get', 'delete'], permission_classes=[IsAuthenticated])
    def set(self, request, pk=None):
        if request.user.is_superuser:
            play_list = get_object_or_404(PlayList, pk=pk)
        else:
            username = request.user.username
            user = get_object_or_404(User, username=username)
            play_list = get_object_or_404(PlayList, pk=pk, user=user)
        serializer = PlayListSerializer(data=request.data)
        if serializer.is_valid():
            play_list.title = serializer.validated_data['title']
            play_list.index = serializer.validated_data['index']
            play_list.save()
            return Response({'status': 'Done!'})
        else:
            return Response(serializer.errors)

