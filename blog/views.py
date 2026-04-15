from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Post, Tag


class IndexView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(is_draft=False)


class PostListView(ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(is_draft=False)


class PostDetailView(DetailView):
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(is_draft=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        context['prev_post'] = (
            Post.objects.filter(is_draft=False, created_at__lt=post.created_at)
            .order_by('-created_at')
            .first()
        )
        context['next_post'] = (
            Post.objects.filter(is_draft=False, created_at__gt=post.created_at)
            .order_by('created_at')
            .first()
        )
        return context


class TagPostsView(ListView):
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(tags=self.tag, is_draft=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class SearchView(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.query = self.request.GET.get('q', '').strip()
        if not self.query:
            return Post.objects.none()
        return Post.objects.filter(
            Q(title__icontains=self.query) | Q(content__icontains=self.query),
            is_draft=False,
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        return context
