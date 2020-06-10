from django.urls import re_path
from news.views import NewPostView, PostView, DeletePostView, UpdatePostView, DeleteCommentView, AboutView


urlpatterns = [
    re_path('newpost', NewPostView.as_view(), name='newpost'),
    re_path('postdetail/(?P<pk>\d+)', PostView.as_view(), name='postdetail'),
    re_path('postdelete/(?P<pk>\d+)', DeletePostView.as_view(), name='postdelete'),
    re_path('postupdate/(?P<pk>\d+)', UpdatePostView.as_view(), name='postupdate'),
    re_path('commentdelete/(?P<pk>\d+)', DeleteCommentView.as_view(), name='commentdelete'),
    re_path('about', AboutView.as_view(), name='about'),
]
