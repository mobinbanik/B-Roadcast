from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

] + static(settings.UPLOAD_URL, document_root=settings.UPLOAD_ROOT)
