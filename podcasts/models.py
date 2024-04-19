import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.html import mark_safe

from abc import abstractmethod


UserModel = get_user_model()


def get_episode_path(instance, file_name):
    return "uploads/channels/{0}/{1}/{2}/{3}/episodes/{4}/{5}".format(
        instance.channel.created_at.year,
        instance.channel.created_at.month,
        instance.channel.created_at.day,
        instance.channel.slug,
        instance.session,
        file_name,
    )


def get_channel_path(instance, file_name):
    return "uploads/channels/{0}/{1}/{2}/{3}/{4}".format(
        instance.created_at.year,
        instance.created_at.month,
        instance.created_at.day,
        instance.slug,
        file_name,
    )


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    @abstractmethod
    def __str__(self):
        raise NotImplementedError('Implement __str__ method')

    class Meta:
        abstract = True


class User(UserModel):
    user_id = models.BigAutoField(primary_key=True)
    about = models.TextField()
    birth_date = models.DateField()
    gender = models.CharField(max_length=32)
    location = models.CharField(max_length=127)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class PlayList(models.Model):
    title = models.CharField(max_length=127)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='play_lists',
    )
    index = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Play List'
        verbose_name_plural = 'Play Lists'


class Channel(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    channel_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to=get_channel_path)
    view_count = models.IntegerField(default=0)
    subscribe_count = models.IntegerField(default=0)
    session_count = models.IntegerField(default=1)
    creator = models.ForeignKey(
        'User', on_delete=models.PROTECT, related_name='channels',
    )

    def img_preview(self):
        try:
            return mark_safe(f'<img src = "{self.thumbnail.url}" style="max-width:200px; max-height:200px"/>')
        except Exception as e:
            return e.__str__()

    def __str__(self):
        return self.title


# class Like(models.Model):
#     like_count = models.IntegerField(default=0)
#     dislike_count = models.IntegerField(default=0)
#     # Save user id
#     detail = models.TextField()
#
#     def __str__(self):
#         return f'{self.like_count}'


class Episode(BaseModel):
    title = models.CharField(max_length=255)
    episode_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(null=True, blank=True)
    channel = models.ForeignKey(
        'Channel', on_delete=models.PROTECT, related_name='episodes',
    )
    session = models.IntegerField(default=1)
    view_count = models.IntegerField(default=0)

    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    # Save user id
    action_detail = models.TextField(null=True, blank=True)

    duration = models.DurationField(null=True, blank=True)

    audio_file = models.FileField(
        upload_to=get_episode_path
    )
    thumbnail = models.ImageField(
        upload_to=get_episode_path
    )

    def img_preview(self):
        try:
            return mark_safe(f'<img src = "{self.thumbnail.url}" style="max-width:200px; max-height:200px"/>')
        except Exception as e:
            return e.__str__()

    def __str__(self):
        return self.title


class Comment(BaseModel):
    text = models.TextField()
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=False)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='user_comments',
    )
    episode = models.ForeignKey(
        'Episode', on_delete=models.CASCADE, related_name='episode_comments',
    )

    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    # Save user id
    action_detail = models.TextField(null=True, blank=True)

    is_reply = models.BooleanField(default=False)
    reply_to = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='episodes')

    def __str__(self):
        return self.user.username + ' comment'


class ItemInPlayList(models.Model):
    order = models.IntegerField()
    play_list = models.ForeignKey(
        'PlayList', on_delete=models.CASCADE, related_name='items',
    )
    episode = models.ForeignKey(
        'Episode', on_delete=models.CASCADE, related_name='item_in_playlists'
    )

    def __str__(self):
        return f'{self.order} : {self.episode.title}'


class UserChannel(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='subscribed_channels',
    )
    channel = models.ForeignKey(
        'Channel', on_delete=models.CASCADE, related_name='users',
    )

    def __str__(self):
        return f'{self.user.username} -> {self.channel.slug}'


class View(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='views',
    )
    channel = models.ForeignKey(
        'Channel', on_delete=models.CASCADE, related_name='views'
    )

    def __str__(self):
        return f'{self.user.username} saw {self.channel.slug}'


class Listen(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='listens',
    )
    episode = models.ForeignKey(
        'Episode', on_delete=models.CASCADE, related_name='listeners',
    )
    minute = models.DurationField()

    def __str__(self):
        return f'{self.user.username} listened to {self.episode.episode_id}'
