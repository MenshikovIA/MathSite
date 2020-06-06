from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions
from django import forms
from register.models import MyUser


class RegisterForm(UserCreationForm):

    username = forms.CharField(label='Логин', max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Sherlock"}))
    first_name = forms.CharField(label='Имя', max_length=30, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Джон"}))
    last_name = forms.CharField(label='Фамилия', max_length=30, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Уотсон"}))
    email = forms.EmailField(label='E-mail', max_length=254,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "hello@gmail.com"}))
    password1 = forms.CharField(label='Пароль:', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль:', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class LoadAvatarForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('avatar',)

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:

            # validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, GIF or PNG image.')

            # validate file size
            if avatar._size > 4 * 1024 * 1024:
                raise forms.ValidationError(u'Avatar file size may not exceed 4mb.')

            w, h = get_image_dimensions(avatar)

            # validate dimensions
            max_width = max_height = 500
            if w > max_width or h > max_height:
                raise forms.ValidationError(u'Avatar sizes may not exceed 1000px')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar
