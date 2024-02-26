from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
import json

from .models import *

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("explore"))
        else:
            return render(request, "blog/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "blog/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "blog/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "blog/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("explore"))
    else:
        return render(request, "blog/register.html")
    
def create_post(request):
    if request.method == "POST":

        user = request.user
        content = request.POST["content"]
        image = request.POST["image"]
        location = request.POST["location"]



        new_post = Post(
            user= user,
            content= content,
            image= image,
            location= location
            )
        new_post.save()

        return HttpResponseRedirect(reverse("explore"))
    else:
        return render(request, "blog/create_post.html")
    

def explore (request):
    posts = Post.objects.all().order_by("id").reverse()
        
    likes = Like.objects.all()
    liked_posts = []

    try:
        for like in likes:
            if like.user.id == request.user.id:
                liked_posts.append(like.post.id)
    except:
        liked_posts = []
    
    return render(request, "blog/explore.html", {
        "posts": posts,
        "liked_posts": liked_posts
    })

def like(request, post_id):
    # Like a post
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Like(user=user, post=post)
    if Like.objects.filter(user=user, post=post).exists():
        pass
    else:
        like.save()

    return HttpResponseRedirect(reverse("explore"))

def unlike(request, post_id):
    # Unlike a post
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Like.objects.get(user=user, post=post)
    like.delete()

    return HttpResponseRedirect(reverse("explore"))
    

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

def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    followers = Follow.objects.filter(following=user).count()
    following = Follow.objects.filter(follower=user).count()
    posts = Post.objects.filter(user=user).order_by("id").reverse()
    liked_posts = Like.objects.filter(user=user).values_list('post_id', flat=True)
    
    try:
        Follow.objects.get(follower=request.user, following=user)
        is_following = True
    except Follow.DoesNotExist:
        is_following = False
        
    return render(request, "blog/profile.html", {
        "posts": posts,
        "username": user.username,
        "user_profile": user,
        "followers": followers,
        "following": following,
        "is_following": is_following,
        "liked_posts": liked_posts
    })


def edit_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == "POST":
        content = request.POST["content"]
        image = request.POST["image"]
        location = request.POST["location"]

        post.content = content
        post.image = image
        post.location = location
        post.save()

        return redirect('explore')
    else:

        return render(request, 'blog/edit_post.html', {'post': post})

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

def following_page(request):
    user = User.objects.get(pk=request.user.id)
    following = Follow.objects.filter(follower=user)
    posts = Post.objects.filter(user__in=following.values("following")).order_by("-timestamp")
    liked_posts = Like.objects.filter(user=user).values_list('post_id', flat=True)

    return render(request, "blog/following.html", {
        "posts": posts,
        "liked_posts": liked_posts
    })

def edit_account(request):
    user = request.user

    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        bio = request.POST.get('bio', '')

        # Update user attributes if provided
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.set_password(password)
        if bio:
            user.bio = bio
            
        user.save()  # Save the updated user object

        return redirect('profile', user_id=user.id)  # Redirect to the profile page after editing

    return render(request, 'blog/edit_account.html', {'user': user})

def post(request, post_id):
    user = request.user
    post = Post.objects.get(pk=post_id)
    liked_posts = Like.objects.filter(user=user).values_list('post_id', flat=True)
    
    return render(request, "blog/post.html", {
    "post": post,
    "comments": Comment.objects.filter(post_id=post_id),
    "user": request.user,
    "liked_posts": liked_posts
    })

def add_comment(request, post_id):
    # Create new comment
    new_comment = Comment(
        author=request.user,
        post=Post.objects.get(pk=post_id),
        comment=request.POST["comment"]
        )
    new_comment.save()

    return HttpResponseRedirect(reverse("post", args=(post_id,)))

def delete_post(request, post_id):
    user = request.user
    post = Post.objects.get(pk=post_id)

    post.delete()

    return redirect('profile', user_id=user.id)