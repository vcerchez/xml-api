from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import XMLUploadView, DatabaseContentView

urlpatterns = [
    path("api/upload/", XMLUploadView.as_view(), name="xml-upload"),
    path('api/db-view/', DatabaseContentView.as_view({'get': 'list'}), name="db-view"),
]
