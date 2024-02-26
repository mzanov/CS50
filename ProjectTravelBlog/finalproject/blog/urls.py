from django.urls import path

from . import views

urlpatterns = [
    path("", views.explore, name="explore"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("like/<int:post_id>", views.like, name="like"),
    path("unlike/<int:post_id>", views.unlike, name="unlike"),
    path("likes/<int:user_id>", views.likes, name="likes"),
    path("like_count/<int:post_id>", views.like_count, name="like_count"),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("following", views.following_page, name="following"),
    path("edit_account", views.edit_account, name="edit_account"),
    path("post/<int:post_id>", views.post, name="post"),
    path("add_comment/<post_id>", views.add_comment, name="add_comment"),
    path("delete_post/<post_id>", views.delete_post, name="delete_post")
]
