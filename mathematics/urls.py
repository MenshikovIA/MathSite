from django.urls import re_path
from mathematics.views import SpiralsView, FractalsView, HyperboloidView


urlpatterns = [
    re_path('spirals', SpiralsView.as_view(), name='spirals'),
    re_path('fractals', FractalsView.as_view(), name='fractals'),
    re_path('hyperboloid', HyperboloidView.as_view(), name='hyperboloid'),
]