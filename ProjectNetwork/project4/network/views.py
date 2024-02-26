from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    posts = Post.objects.all().order_by("id").reverse()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
        
    likes = Like.objects.all()
    liked_posts = []

    try:
        for like in likes:
            if like.user.id == request.user.id:
                liked_posts.append(like.post.id)
    except:
        liked_posts = []
    
    return render(request, "network/index.html", {
        "posts": page_obj,
        "liked_posts": liked_posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def new_post(request):
    if request.method == 'POST':
        user = request.user
        content = request.POST["content"]
        post = Post(user = user, content = content)
        post.save()

        return HttpResponseRedirect(reverse("index"))
    
def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    followers = Follow.objects.filter(following=user).count()
    following = Follow.objects.filter(follower=user).count()
    posts = Post.objects.filter(user=user).order_by("id").reverse()
    
    try:
        Follow.objects.get(follower=request.user, following=user)
        is_following = True
    except Follow.DoesNotExist:
        is_following = False

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
        
    return render(request, "network/profile.html", {
        "posts": page_obj,
        "username": user.username,
        "user_profile": user,
        "followers": followers,
        "following": following,
        "is_following": is_following
    })

def following(request):
    user = User.objects.get(pk=request.user.id)
    following = Follow.objects.filter(follower=user)
    posts = Post.objects.filter(user__in=following.values("following")).order_by("-timestamp")

    # Paginate posts
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
        
    return render(request, "network/following.html", {
        "posts": page_obj
    })

def follow(request):
    requested_user = request.POST["user_follow"]
    follow_request = User.objects.get(username=requested_user)
    user = User.objects.get(pk=request.user.id)
    follow = Follow(follower=user, following=follow_request)
    follow.save()

    return HttpResponseRedirect(reverse("profile", args=(follow_request.id,)))

def unfollow(request):
    requested_user = request.POST["user_unfollow"]
    follow_request = User.objects.get(username=requested_user)
    user = User.objects.get(pk=request.user.id)
    follow = Follow.objects.get(follower=user, following=follow_request)
    follow.delete()

    return HttpResponseRedirect(reverse("profile", args=(follow_request.id,)))

def edit_post(request, post_id):
    if request.method == "POST":
        # Edit a post
        content = json.loads(request.body)["content"]
        post = Post.objects.get(pk=post_id)
        post.content = content
        post.save()

        return HttpResponseRedirect(reverse("index"))
    
def like(request, post_id):
    # Like a post
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Like(user=user, post=post)
    if Like.objects.filter(user=user, post=post).exists():
        pass
    else:
        like.save()

    return HttpResponseRedirect(reverse("index"))

def unlike(request, post_id):
    # Unlike a post
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Like.objects.get(user=user, post=post)
    like.delete()

    return HttpResponseRedirect(reverse("index"))
    

def like_count(request, post_id):
    post = Post.objects.get(pk=post_id)
    like_count = Like.objects.filter(post=post).count()

    return HttpResponse(json.dumps({"like_count": like_count}), content_type="application/json")

def likes(request, user_id):
    # All user's liked posts
    likes = Like.objects.all()
    liked_posts = []

    try:
        for like in likes:
            if like.user.id == user_id:
                liked_posts.append(like.post.id)
    except:
        liked_posts = []

    return HttpResponse(json.dumps({"liked_posts": liked_posts}), content_type="application/json")
