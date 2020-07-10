from django.urls import re_path, include
from social_app.views import TestView, FriendsView


urlpatterns = [
    re_path('index', TestView.as_view(), name='login'),
    re_path('friends', FriendsView.as_view(), name='login'),
    re_path('', include('social_django.urls', namespace='social')),
]
