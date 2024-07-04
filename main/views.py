from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Tweet, Like
from .forms import TweetForm, CommentForm

def home(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'main/home.html', {'tweets': tweets})

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'main/tweet_list.html', {'tweets': tweets})

@login_required
def tweet_detail(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    comments = tweet.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.tweet = tweet
            comment.save()
            return redirect('tweet_detail', tweet_id=tweet_id)
    else:
        comment_form = CommentForm()
    return render(request, 'main/tweet_detail.html', {
        'tweet': tweet,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.author = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'main/tweet_create.html', {'form': form})

@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    like, created = Like.objects.get_or_create(tweet=tweet, user=request.user)
    if not created:
        like.delete()
    return redirect('home')