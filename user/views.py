from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import UserProfile
from news.models import Category, Comment, Like
from user.forms import UserUpdateForm, ProfileUpdateForm


def index(request):

    categories = Category.objects.all()
    profile = UserProfile.objects.get(user=request.user)
    context = {
        'categories': categories,
        'profile': profile,
        'page': 'Profile',

    }
    return render(request, 'user_profile.html', context)


def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return HttpResponseRedirect('/user')
    else:
        categories = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'categories': categories,
            'user_form': user_form,
            'page': 'profile update',
            'profile_form': profile_form,
        }
        return render(request, 'user_update.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct thr errors below:<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        categories = Category.objects.all()
        form = PasswordChangeForm(request.user)
        context = {
            'form': form,
            'categories': categories,
            'page': 'password update',
        }
        return render(request, 'change_password.html', context)


def user_comments(request):
    comments = Comment.objects.filter(user_id=request.user.id)
    categories = Category.objects.all()
    context = {
        'comments': comments,
        'categories': categories,
        'page': 'my comments',
    }
    return render(request, 'user_comments.html', context)


def delete_comment(request, id):
    Comment.objects.filter(id=id, user_id=request.user.id).delete()
    messages.success(request, "Comment Deleted Successfully!")
    return HttpResponseRedirect('/user/comments')


def user_likes(request):
    likes = Like.objects.filter(user_id=request.user.id)
    categories = Category.objects.all()
    context = {
        'likes': likes,
        'categories': categories,
        'page': 'my likes',
    }
    return render(request, 'user_likes.html', context)