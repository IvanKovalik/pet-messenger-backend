from .views import ListNews, DetailNews, ListPosts, DetailPost, ListUsers

from django.urls import path

urlpatterns = [
    path('news/', ListNews.as_view()),
    path('news/<str:pk>', DetailNews.as_view()),
    
    path('posts/', ListPosts.as_view()),
    path('posts/<str:pk>', DetailPost.as_view()),
    
    path('users/', ListUsers.as_view()),
]