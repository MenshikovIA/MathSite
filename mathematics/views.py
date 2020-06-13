from django.shortcuts import render
from django.views import View


class SpiralsView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, 'spirals.html', context={})


class FractalsView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, 'fractals.html', context={})


class HyperboloidView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, 'hyperboloid.html', context={})
