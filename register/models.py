from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='register/profile_pics/', blank=True)

    def __str__(self):
        return self.user.username
