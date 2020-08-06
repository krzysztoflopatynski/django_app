from . import views
from django.urls import path


app_name='importers'

urlpatterns = [
    path("", views.file_upload, name="upload"),
]

