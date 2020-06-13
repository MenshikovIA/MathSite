from django.urls import re_path
from register.views import SignUpView, LoginView, LogoutView, ProfileView, UserInfoView


urlpatterns = [
    re_path('login', LoginView.as_view(), name='login'),
    re_path('logout', LogoutView.as_view(), name='logout'),
    re_path('signup', SignUpView.as_view(), name='signup'),
    re_path('profile', ProfileView.as_view(), name='profile'),
    re_path('userinfo/(?P<pk>\d+)', UserInfoView.as_view(), name='userinfo'),
]

