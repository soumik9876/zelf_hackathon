from django.urls import path

from social_content.api.v1.views import ContentAuthorAPIView

urlpatterns = [
    path('content-author/', ContentAuthorAPIView.as_view(), name='content-author')
]
