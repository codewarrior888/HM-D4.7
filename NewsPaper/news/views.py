from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .filters import PostFilter
from .forms import PostForm


class NewsList(ListView):
    model = Post
    ordering = '-post_time'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(post_genre='NW')


class ArticlesList(ListView):
    model = Post
    ordering = '-post_time'
    template_name = 'articles.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(post_genre='AR')


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'pk'


class PostSearch(ListView):
    model = Post
    ordering = '-post_time'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_genre = 'NW'
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_genre = 'AR'
        return super().form_valid(form)


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

    def get_object(self, queryset=None):
        obj = get_object_or_404(Post, pk=self.kwargs['pk'])
        if obj.post_genre != 'NW':
            raise Http404("Такой новости нет.")
        return obj


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('articles_list')

    def get_object(self, queryset=None):
        obj = get_object_or_404(Post, pk=self.kwargs['pk'])
        if obj.post_genre != 'AR':
            raise Http404("Такой статьи нет.")
        return obj


class ArticleEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Post, pk=self.kwargs['pk'])
        if obj.post_genre != 'AR':
            raise Http404("Такой статьи нет.")
        return obj


class NewsEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Post, pk=self.kwargs['pk'])
        if obj.post_genre != 'NW':
            raise Http404("Такой новости нет.")
        return obj
