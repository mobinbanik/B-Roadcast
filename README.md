
    admin/
    [name='home']
    logout/ [name='logout']
    login/ [name='login']
    register/ [name='register']
    ^uploads/(?P<path>.*)$
    api/ episode/ ^$ [name='episode-list']
    api/ episode/ ^\.(?P<format>[a-z0-9]+)/?$ [name='episode-list']
    api/ episode/ ^get/$ [name='episode-get']
    api/ episode/ ^get\.(?P<format>[a-z0-9]+)/?$ [name='episode-get']
    api/ episode/ ^(?P<pk>[^/.]+)/$ [name='episode-detail']
    api/ episode/ ^(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='episode-detail']
    api/ episode/ ^(?P<pk>[^/.]+)/id/$ [name='episode-id']
    api/ episode/ ^(?P<pk>[^/.]+)/id\.(?P<format>[a-z0-9]+)/?$ [name='episode-id']
    api/ episode/ [name='api-root']
    api/ episode/ <drf_format_suffix:format> [name='api-root']
    api/ channel/
    api/ playlist/
