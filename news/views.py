from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from news.models import CommentForm, Comment, Like, News


def index(request):
    return HttpResponse("news page")


@login_required(login_url='/login')
def addcomment(request, post_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user
            data = Comment()
            data.user_id = current_user.id
            data.post_id = post_id
            data.comment = form.cleaned_data['comment']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Your comment submitted successfully!")
            return HttpResponseRedirect(url)
    messages.warning(request, "An error occurred while attempting to submit your comment!")
    return HttpResponseRedirect(url)


def like(request, post_id):
    url = request.META.get('HTTP_REFERER')

    likes = Like.objects.filter(post_id=post_id)
    users = []
    for like in likes:
        users.append(like.user)
    if request.user in users:
        likes.get(user_id=request.user.id).delete()
    else:
        new_like = Like()
        new_like.user = request.user
        new_like.post = News.objects.get(id=post_id)
        new_like.save()
        messages.success(request, "Liked")
        return HttpResponseRedirect(url)
    messages.warning(request, "error")
    return HttpResponseRedirect(url)