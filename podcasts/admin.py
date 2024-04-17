from django.contrib import admin
from django.contrib.admin import register

from .models import (
    BaseModel,
    User,
    PlayList,
    Channel,
    Like,
    Episode,
    Comment,
    ItemInPlayList,
    UserChannel,
    View,
    Listen,
)


# Register your models here.
@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'first_name',
        'last_name',
        'username',
        'gender',
        'location',
    )
    list_filter = (
        'is_active',
        'gender',
        'location',
        'birth_date',
    )
    search_fields = (
        'user_id',
        'first_name',
        'last_name',
        'username',
        'about',
        'location',
    )


@register(PlayList)
class PlayListAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'user',
        'index',
    )
    search_fields = (
        'user__username',
        'title',
    )


@register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = (
        'img_preview',
        'channel_id',
        'title',
        'creator',
        'is_active',
    )
    list_filter = (
        'is_active',
    )
    search_fields = (
        'title',
        'description',
        'creator__username',
    )


@register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'like_count',
        'dislike_count',
        'detail',
    )


@register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = (
        'img_preview',
        'episode_id',
        'title',
        'description',
        'duration',
        'channel',
        'session',
        'view_count',
        'like',
        'is_active',
    )
    list_filter = (
        'is_active',
    )
    search_fields = (
        'title',
        'episode_id',
        'description',
        'channel__title',
        'channel__description',
        'channel__creator__username',
    )


@register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'comment_id',
        'user',
        'text',
        'is_active',
        'episode',
        'is_reply',
    )
    list_filter = (
        'is_reply',
        'is_active',
    )
    search_fields = (
        'text',
        'user__username',
        'episode__title',
    )


@register(ItemInPlayList)
class ItemInPlayListAdmin(admin.ModelAdmin):
    list_display = (
        'play_list',
        'episode',
        'order',
    )
    list_filter = (
        'play_list',
    )
    search_fields = (
        'play_list__title',
        'episode__title',
        'episode__description',
    )


@register(UserChannel)
class UserChannelAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'channel',
    )
    list_filter = (
        'channel',
    )
    search_fields = (
        'channel__title',
        'user__username',
    )


@register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'channel',
    )
    list_filter = (
        'channel',
    )
    search_fields = (
        'channel__title',
        'user__username',
    )


@register(Listen)
class ListenAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'episode',
        'minute',
    )
    list_filter = (
        'user',
        'episode',
    )
    search_fields = (
        'user__username',
        'episode__title',
    )
