from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import requests
import json


class TestView(View):
    def get(self, request):
        context = {}
        return render(request, 'social_app/test.html', context=context)


class FriendsView(View):
    def get(self, request):
        social_user = request.user.social_auth.filter(provider='vk-oauth2').first()
        context = {}
        if social_user:
            friends = requests.get('https://api.vk.com/method/friends.get',
                                   params=dict(user_ids=social_user.uid,
                                               fields="photo_100,domain",
                                               order='random',
                                               access_token=social_user.extra_data['access_token'],
                                               count=5,
                                               v="5.120"))
            context['friends'] = friends.json()['response']['items']

            vk_user = requests.get('https://api.vk.com/method/users.get',
                                   params=dict(user_ids=social_user.uid,
                                               fields="photo_200,domain,online",
                                               access_token=social_user.extra_data['access_token'],
                                               v="5.120"))
            context['vk_user'] = vk_user.json()['response'][0]

        return render(request, 'social_app/friends.html', context=context)
