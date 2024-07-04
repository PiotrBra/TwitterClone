from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tweet/create/', views.tweet_create, name='tweet_create'),
    path('tweet/<int:tweet_id>/', views.tweet_detail, name='tweet_detail'),
    path('tweet/<int:tweet_id>/like/', views.like_tweet, name='like_tweet'),
    path('tweets/', views.tweet_list, name='tweet_list'),
]
