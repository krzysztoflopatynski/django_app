from . import views
from django.urls import path


app_name='reports'

urlpatterns = [
    path("", views.report_view, name="report_view"),
]

