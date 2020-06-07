from django import forms
from news.models import (Post, Comment)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'description', )

    title = forms.CharField(widget=forms.TextInput(
        attrs={'label': '', 'class': 'form-control', 'placeholder': 'Заголовок поста'}
    ))
    description = forms.CharField(widget=forms.TextInput(
        attrs={'label': '', 'class': 'form-control', 'placeholder': 'Описание (будет отображаться на главной странице)'}
    ))
    text = forms.CharField(label='', widget=forms.Textarea(attrs={'id': 'postarea'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )

    text = forms.CharField(widget=forms.Textarea(attrs={'id': 'commentarea'}))
