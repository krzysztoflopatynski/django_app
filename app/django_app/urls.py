from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

from .views import welcome


urlpatterns = [
    path('', welcome, name="welcome"),
    path('upload/', include('importers.urls')),
    path('report/', include('reports.urls')),
    path("admin/", admin.site.urls),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
