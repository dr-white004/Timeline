from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    post = models.CharField(max_length=300)
    timing = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, symmetrical=False, blank=True, related_name="users_liked")

    def count_likes(self):
        return self.liked_by.count()

    class Meta:
        ordering = ['-timing']

    
  

class Following(models.Model):
    follow = models.ManyToManyField(User, blank=True, related_name="watch")
    owner = models.CharField(max_length=32, unique=True)
   
    def __str__(self):
       return f"{self.owner} has followers"

class imfollowing(models.Model):
    imfollow = models.ManyToManyField(User, blank=True,related_name="watching")
    ifollowed = models.CharField(max_length=32, unique = True)

    def __str__(self):
       return f"{self.ifollowed} is following"


