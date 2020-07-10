from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from news.forms import PostForm, CommentForm
from news.models import Post, Comment


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


class PostView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        pk = kwargs['pk']
        post = get_object_or_404(Post, id=pk)
        comments = Comment.objects.filter(post_id=pk).order_by('-created_date')
        return render(request, 'post_detail.html', context={'post': post, 'comments': comments, 'form': CommentForm()})

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        pk = kwargs['pk']
        post = get_object_or_404(Post, id=pk)
        if request.method == 'POST':
            if form.is_valid():
                comm = form.save(commit=False)
                comm.post = post
                comm.author = request.user
                comm.save()
        comments = Comment.objects.filter(post_id=pk).order_by('-created_date')
        return render(request, 'post_detail.html', context={'post': post, 'comments': comments, 'form': CommentForm()})


class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('index')


class DeleteCommentView(View):
    def get(self, request, *args, **kwargs):
        comment_id = kwargs['pk']
        comment_obj = get_object_or_404(Comment, id=comment_id)
        post_id = comment_obj.post_id
        if request.user.id == comment_obj.author.id or request.user.is_staff:
            comment_obj.delete()
        return redirect('postdetail', post_id)


class UpdatePostView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Post
    success_url = reverse_lazy('index')
    template_name = 'update_post.html'
    form_class = PostForm


class AboutView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, 'about.html')
