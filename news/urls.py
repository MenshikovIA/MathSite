from django.urls import re_path, path
from news.views import MainPageView, NewPostView, PostView


urlpatterns = [
    re_path('newpost', NewPostView.as_view(), name='newpost'),
    re_path('postdetail/(?P<pk>\d+)', PostView.as_view(), name='postdetail'),
]
