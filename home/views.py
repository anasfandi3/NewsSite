from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

from home.models import Setting, ContactFormMessage, ContactForm
from news.models import News, Category, Images, Comment, Like


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = News.objects.all()[:3]
    hot_news = News.objects.all()[:4]
    latest_news = News.objects.all().order_by('-id')[:4]
    random_news = News.objects.all().order_by('?')[:4]
    today_news = News.objects.all().order_by('-id') [:4]
    categories = Category.objects.all()
    context = {'setting': setting,
               'sliderdata': sliderdata,
               'latest_news': latest_news,
               'hot_news': hot_news,
               'random_news': random_news,
               'categories': categories,
               'today_news': today_news,
               }
    return render(request, 'index.html', context)


def about(request):
    setting = Setting.objects.get(pk=1)
    categories = Category.objects.all()
    context = {'setting': setting,
               'page': 'about',
               'categories': categories,
               }
    return render(request, 'about.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "your message had been sent successfully!")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    #form = ContactForm()
    categories = Category.objects.all()
    context = {'setting': setting,
               'page': 'contact',
               'categories': categories,
               }
    return render(request, 'contact.html', context)


def category_news(request, id, slug):
    news = News.objects.filter(category_id=id)
    categories = Category.objects.all()
    category = Category.objects.get(id=id)
    context = {'news': news,
               'categories': categories,
               'category': category,
               'page': 'category_news'
               }
    return render(request, 'news.html', context)


def post_detail(request, id, slug):
    categories = Category.objects.all()
    post = News.objects.get(id=id)
    comments = Comment.objects.filter(post_id=id)
    likes_count = Like.objects.filter(post_id=id).count()
    images = Images.objects.filter(news_id=id)
    context = {
                'post': post,
                'categories': categories,
                'comments': comments,
                'images': images,
                'likes_count': likes_count,
                'page': 'single_post'
               }

    return render(request, 'post.html', context)
