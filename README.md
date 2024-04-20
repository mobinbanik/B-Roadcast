# B-Roadcast

B-Roadcast  is a Django application
for podcast website.

## Installation

1. Install the required packages listed in `requirements.txt`:
```pip install -r requirements.txt```
2. Create and configure your `local_settings.py` file based on the provided `sample_settings.py`. This file should contain settings specific to your local environment, such as Celery broker URL and timezone.

3. Migrate the database:
```python manage.py migrate```
4. Create a superuser for accessing the admin panel:
```python manage.py createsuperuser```

## URLs
Use the provided URLs for accessing different functionalities:
- `/`: home
- `/logout/`: logout
- `/login/`: login
- `/register/`: register



```python
urlpatterns = [
    path('episode/', include(router_episode.urls)),
    path('channel/', include(router_channels.urls)),
    path('playlist/', include(router_play_list.urls)),
    path('comment/', include(router_comment.urls)),
    path('followers/', include(router_followers.urls)),
    path('users/', include(router_users.urls)),
] 
```


# GitHub
https://github.com/mobinbanikarim
