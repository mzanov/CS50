from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    pass
   

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    content = models.TextField()
    image = models.CharField(max_length=1000, blank=True, null=True,)
    location = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"{self.user} posted post #{self.id} on {self.date.strftime('%b %d %Y, %I:%M %p')}"
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return f"{self.follower} is following {self.following}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like_user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="like_post")

    def __str__(self):
        return f"{self.user} liked post #{self.post.id}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comment")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name="post_comment")
    comment = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.author} commented on {self.post}'