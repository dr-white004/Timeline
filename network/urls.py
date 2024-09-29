
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("profile/<str:nm>", views.profile, name="profile"),
    path("follow/<str:nm>", views.follow, name="follow"),
    path("followingfunc", views.followingfunc, name="followingfunc"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("post/<int:post_id>/like", views.like_post, name="like_post")
   
]

 



