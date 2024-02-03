from django.urls import path

from social_content.api.v1.views import ContentAuthorAPIView, StatsDataAPIView, ContentByDate, ContentByPlatform

urlpatterns = [
    path('content-author/', ContentAuthorAPIView.as_view(), name='content-author'),
    path('stats/', StatsDataAPIView.as_view(), name='stats'),
    path('content-by-date/', ContentByDate.as_view(), name='content-by-date'),
    path('content-by-platform/', ContentByPlatform.as_view(), name='content-by-platform'),
]
