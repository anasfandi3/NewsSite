from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import UserProfile
from news.models import Category, Comment, Like, News, NewsForm, ImageForm, Images
from user.forms import UserUpdateForm, ProfileUpdateForm


@login_required(login_url='/login')
def index(request):

    categories = Category.objects.filter(status='True')
    profile = UserProfile.objects.get(user=request.user)
    context = {
        'categories': categories,
        'profile': profile,
        'page': 'Profile',

    }
    return render(request, 'user_profile.html', context)


@login_required(login_url='/login')
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
        categories = Category.objects.filter(status='True')
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'categories': categories,
            'user_form': user_form,
            'page': 'profile update',
            'profile_form': profile_form,
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login')
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
        categories = Category.objects.filter(status='True')
        form = PasswordChangeForm(request.user)
        context = {
            'form': form,
            'categories': categories,
            'page': 'password update',
        }
        return render(request, 'change_password.html', context)


@login_required(login_url='/login')
def user_comments(request):
    comments = Comment.objects.filter(user_id=request.user.id, status='True')
    categories = Category.objects.filter(status='True')
    context = {
        'comments': comments,
        'categories': categories,
        'page': 'my comments',
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')
def delete_comment(request, id):
    Comment.objects.filter(id=id, user_id=request.user.id).delete()
    messages.success(request, "Comment Deleted Successfully!")
    return HttpResponseRedirect('/user/comments')


@login_required(login_url='/login')
def user_likes(request):
    likes = Like.objects.filter(user_id=request.user.id)
    categories = Category.objects.all()
    context = {
        'likes': likes,
        'categories': categories,
        'page': 'my likes',
    }
    return render(request, 'user_likes.html', context)


@login_required(login_url='/login')
def user_posts(request):
    posts = News.objects.filter(user_id=request.user.id, status='True')
    categories = Category.objects.all()
    context = {
        'posts': posts,
        'categories': categories,
        'page': 'my posts',
    }
    return render(request, 'user_posts.html', context)


@login_required(login_url='/login')
def user_new_post(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            data = News()
            data.user = request.user
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.category = form.cleaned_data['category']
            data.content = form.cleaned_data['content']
            data.slug = form.cleaned_data['slug']
            data.status = 'False'
            data.save()
            messages.success(request, 'Post saved successfully!')
            return HttpResponseRedirect('/user/posts')
        else:
            messages.warning(request, 'Content From Error :' + str(form.errors))
            return HttpResponseRedirect('/')
    else:
        categories = Category.objects.all()
        form = NewsForm()
        context = {
            'categories': categories,
            'form': form,
        }
        return render(request, 'user_new_post.html', context)


@login_required(login_url='/login')
def user_edit_post(request, id):
    post = News.objects.get(id=id)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post saved successfully!')
            return HttpResponseRedirect('/user/posts')
        else:
            messages.warning(request, 'Content From Error :' + str(form.errors))
            return HttpResponseRedirect('/')
    else:
        categories = Category.objects.filter(status='True')
        form = NewsForm(instance=post)
        context = {
            'categories': categories,
            'form': form,
        }
        return render(request, 'user_new_post.html', context)


@login_required(login_url='/login')
def user_delete_post(request, id):
    News.objects.filter(id=id, user_id=request.user.id).delete()
    messages.success(request, "deleted successfully!")
    return HttpResponseRedirect('/user/posts')


def user_image_gallery(request, id):
    if request.method == 'POST':
        last_url = request.META.get('HTTP_REFERER')
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = Images()
            data.title = form.cleaned_data['title']
            data.news_id = id
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Image has been saved successfully!')
            return HttpResponseRedirect(last_url)
        else:
            messages.warning(request, 'Form Error:' + str(form.errors))
            return HttpResponseRedirect(last_url)
    else:
        post = News.objects.get(id=id)
        images = []
        try:
            images = Images.objects.filter(news_id=id)
        except:
            pass
        form = ImageForm()
        context = {
            'post': post,
            'images': images,
            'form': form
        }
        return render(request, 'image_gallery.html', context)