from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

from .models import User, Post, Following, imfollowing


def index(request):
    everyPost = Post.objects.all().order_by('id').reverse()


    paginator = Paginator(everyPost, 10)
    page_number = request.GET.get('page')
    post_of_the_page = paginator.get_page(page_number)


    return render(request, "network/index.html",{
        'everyPost': everyPost,
        'post_of_the_page': post_of_the_page,
        
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
            main = Following.objects.create(owner =username )
            main.save()
            mai = imfollowing.objects.create(ifollowed = username)
            mai.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def newpost(request):
    if request.method == "POST":
        ans = request.POST
        user = request.user
        username = request.user.username
        ost = Post.objects.create(post = ans['neww'], user=user )
        ost.save()
        everyPost = Post.objects.all().order_by('id').reverse()
        paginator = Paginator(everyPost, 5)
        page_number = request.GET.get('page')
        post_of_the_page = paginator.get_page(page_number)
        if Following.objects.filter(owner = username).exists() and imfollowing.objects.filter(ifollowed = username):
            return render(request, "network/index.html",{
             'post_of_the_page': post_of_the_page
            })
        else:
            main = Following.objects.create(owner =username )
            main.save()
            mai = imfollowing.objects.create(ifollowed = username)
            mai.save()
            
            return render(request, "network/index.html",{
                'post_of_the_page': post_of_the_page
                })
    else:
        return render(request, "network/newpost.html")



def profile(request, nm):
    global check
    own = User.objects.get(username=nm)
    data = Following.objects.get(owner = nm)
    info = imfollowing.objects.get(ifollowed= nm)
    print(data)
    #Those following user
    p = data.follow.all()
    # those user is following
    q = info.imfollow.all() 
    allpost= Post.objects.filter(user = own)

    #for the purpose of displaying edit function to the creator only
    if nm == request.user.username:
        ed = True
    else:
        ed = False

    follower= request.user
    data = Following.objects.get(owner = nm)
    if follower not in data.follow.all() :
        check = False
    else:
        check = True

    return render(request, "network/profile.html",{
        'p': p,
        'nm':nm,
        'q': q,
        'check': check,
        'allpost': allpost,
        'ed':ed
        })

check = False

def follow(request, nm):
    global check
    follower= request.user
    data = Following.objects.get(owner = nm)
    if follower.username == data.owner:
        return HttpResponseRedirect(reverse("profile", args=(nm,)))
    elif follower not in data.follow.all() :
        data.follow.add(follower)
        check = False
    else:
        data.follow.remove(follower)
        check =True

    # to record those follower is following
    followerusername= request.user.username
    beingfollowed = User.objects.get(username = nm)
    info = imfollowing.objects.get(ifollowed = followerusername)

    if beingfollowed not in info.imfollow.all() :
        info.imfollow.add(beingfollowed)
    else:
        info.imfollow.remove(beingfollowed)


    return HttpResponseRedirect(reverse("profile", args=(nm,)))

def followingfunc(request):
    currentuser = request.user.username
    following_users = Following.objects.get(owner=currentuser).follow.all()
    posts = []
    for user in following_users:
        user_posts = Post.objects.filter(user=user)
        posts.extend(list(user_posts))
        
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)


    return render(request, "network/following.html", {
        'posts': posts,
    })

def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=post_id)
        edit_post.post = data["content"]
        edit_post.save()
        return JsonResponse({"message": "Change successfull", "data": data["content"]})

def like_post(request, post_id):
    if request.method == "POST":
        # get post with that id
        post = Post.objects.filter(id=post_id)

        # check if that post exist
        if len(post) == 1:
            post_to_edit = post[0]
            read_json = json.loads(request.body)
            # determine if post is to be liked or unlike
            action = read_json['action']

            # check if post is liked by requesting user
            post_is_liked = request.user in post_to_edit.liked_by.all()

            if action == "like" and not post_is_liked:
                post_to_edit.liked_by.add(request.user)
                post_to_edit.save()
            elif post_is_liked:
                post_to_edit.liked_by.remove(request.user)
                post_to_edit.save()

            like_count = post_to_edit.count_likes()
            like_status = request.user in post_to_edit.liked_by.all()

            response = {'like_count': like_count,
                        'like_status': like_status}

            return JsonResponse(response)