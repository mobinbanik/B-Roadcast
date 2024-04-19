from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import view_podcasts, logout_view, login_view, register_view

urlpatterns = [
    path('', view_podcasts, name='home'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),


] + static(settings.UPLOAD_URL, document_root=settings.UPLOAD_ROOT)
