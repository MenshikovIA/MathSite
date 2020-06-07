from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from news.forms import PostForm, CommentForm
from news.models import Post


class MainPageView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        all_posts = Post.objects.all().order_by('-created_date')

        page = request.GET.get('page', 1)
        paginator = Paginator(all_posts, 6)
        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)
        return render(request, 'index.html',
                      context={'post_list': post_list, 'first_group': post_list[0:3], 'second_group': post_list[3:]})


class NewPostView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    template_name = 'new_post.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse('postdetail', args=(self.object.id,))

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostView(DetailView):
    model = Post
    template_name = 'post_detail.html'

