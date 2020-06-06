from django.urls import re_path
from news.views import MainPageView


urlpatterns = [
    re_path('', MainPageView.as_view(), name='index'),
]
