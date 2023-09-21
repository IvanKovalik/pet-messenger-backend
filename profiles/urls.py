from django.urls import path

from .views import *

urlpatterns = [
    path('profile/<str:uid>/', ProfileView.as_view(), name='profile-page'),
]