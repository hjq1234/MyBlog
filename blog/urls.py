from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('tag/<slug:slug>/', views.TagPostsView.as_view(), name='tag_posts'),
    path('search/', views.SearchView.as_view(), name='search'),
]
