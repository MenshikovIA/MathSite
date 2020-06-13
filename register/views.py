from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, Permission
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from register import forms
from register.models import MyUser


class SignUpView(View):

    success = False

    def get(self, request, *args, **kwargs):
        return render(request, 'signup.html', context={"form": forms.RegisterForm, 'success': self.success})

    def post(self, request, *args, **kwargs):
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, 'signup.html',
                              context={"form": form, "error": "Sorry, this username is occupied!",
                                       'success': self.success})
            else:
                user = form.save()
                user.refresh_from_db()
                login(request, user)
                self.success = True
                try:
                    MyUser.objects.create(user_id=user.id, avatar='register/profile_pics/default.png')
                except Exception:
                    print(Exception)

        return render(request, 'signup.html', context={"form": form, 'success': self.success})


class LogoutView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return redirect('index')


class ProfileView(LoginRequiredMixin, View):
    login_url = 'login'
    form_av = forms.LoadAvatarForm()

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('admin:index')
        else:
            return render(request, 'profile.html', context={'message': '', 'form_av': self.form_av})

    def post(self, request, *args, **kwargs):
        print(request.POST)

        if 'password_button' in request.POST:
            op = request.POST['old_password']
            np1 = request.POST['new_password1']
            np2 = request.POST['new_password2']

            if not check_password(op, encoded=request.user.password):
                message_ps = "Wrong old password"
            elif np1 != np2:
                message_ps = "Passwords don't match"
            elif np1 == op:
                message_ps = "Enter new password"
            else:
                request.user.set_password(np1)
                request.user.save()
                login(request, request.user)
                message_ps = 'Готово'
            return render(request, 'profile.html', context={'message_ps': message_ps, 'form_av': self.form_av})

        elif 'av_button' in request.POST:
            form = forms.LoadAvatarForm(request.POST, request.FILES)
            if form.is_valid() and request.FILES:
                MyUser.objects.filter(user_id=request.user.id).delete()
                current_user = form.save(commit=False)
                current_user.user = request.user
                current_user.avatar = request.FILES['avatar']
                current_user.save()
                message_av = 'Готово'
            else:
                message_av = form.errors
            return render(request, 'profile.html', context={'message_av': message_av, 'form_av': self.form_av})

        elif 'ui_button' in request.POST:

            username = request.POST['username']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']

            username_changed = username != request.user.username

            if not username:
                message_ui = 'Username cannot be empty!'

            elif not email:
                message_ui = 'Email cannot be empty!'

            elif username_changed and User.objects.filter(username=username).exists():
                message_ui = 'Sorry, this username is occupied!'

            else:
                if username_changed:
                    request.user.username = username
                request.user.email = email
                request.user.first_name = first_name
                request.user.last_name = last_name
                request.user.save()
                login(request, request.user)
                message_ui = 'Готово'
            return render(request, 'profile.html', context={'message_ui': message_ui, 'form_av': self.form_av})


class LoginView(View):

    loggedin = False

    def get(self, request, *args, **kwargs):
        return render(request, 'login.html', {'loggedin': self.loggedin, 'error': ''})

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user=user)
            self.loggedin = True
        else:
            return render(request, 'login.html', {'loggedin': self.loggedin, 'error': 'Wrong login or password!'})
        return render(request, 'login.html', {'loggedin': self.loggedin, 'error': ''})


class UserInfoView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        user_id = kwargs['pk']
        userinfo = get_object_or_404(User, id=user_id)
        user_avatar = MyUser.objects.filter(user_id=user_id)
        if user_avatar.exists():
            avatar = user_avatar[0].avatar
        else:
            avatar = 'register/profile_pics/default.png'
        return render(request, 'userinfo.html', context={'userinfo': userinfo, 'avatar': avatar})
