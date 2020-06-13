import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormMessage, ContactForm, UserProfile, FAQ
from news.models import News, Category, Images, Comment, Like


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = News.objects.filter(status='True')[:3]
    special_news = News.objects.filter(special=True, status='True')[:4]
    latest_news = News.objects.filter(status='True').order_by('-id')[:4]
    random_news = News.objects.filter(status='True').order_by('?')[:4]
    today_news = News.objects.filter(status='True').order_by('-id') [:4]
    categories = Category.objects.filter(status='True')

    context = {'setting': setting,
               'sliderdata': sliderdata,
               'latest_news': latest_news,
               'special_news': special_news,
               'random_news': random_news,
               'categories': categories,
               'today_news': today_news,
               }
    return render(request, 'index.html', context)


def about(request):
    setting = Setting.objects.get(pk=1)
    categories = Category.objects.filter(status='True')
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
    categories = Category.objects.filter(status='True')
    context = {'setting': setting,
               'page': 'contact',
               'categories': categories,
               }
    return render(request, 'contact.html', context)


def category_news(request, id, slug):
    category = Category.objects.get(id=id)
    news = find_subs(category)
    categories = Category.objects.filter(status='True')
    context = {'news': news,
               'categories': categories,
               'category': category,
               'page': 'category_news'
               }
    return render(request, 'news.html', context)


def post_detail(request, id, slug):
    categories = Category.objects.all()
    post = News.objects.get(id=id)
    comments = Comment.objects.filter(post_id=id, status='True')
    likes = Like.objects.filter(post_id=id)
    likes_count = likes.count()
    users = []
    for like in likes:
        users.append(like.user)
    if request.user in users:
        liked = "yes"
    else:
        liked = ""
    images = Images.objects.filter(news_id=id)
    context = {
                'post': post,
                'categories': categories,
                'comments': comments,
                'liked': liked,
                'images': images,
                'likes_count': likes_count,
                'page': 'single_post'
               }

    return render(request, 'post.html', context)


def news_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            categories = Category.objects.filter(status='True')
            query = form.cleaned_data['query']
            news = News.objects.filter(title__icontains=query, status='True')
            # return HttpResponse(products)
            context = {'news': news,
                       'categories': categories,
                       'page': 'search',
                       }
            return render(request, 'news_search.html', context)

    return HttpResponseRedirect('/')


def news_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        news = News.objects.filter(title__icontains=q, status='True')
        results = []
        for rs in news:
            news_json = {}
            news_json = rs.title
            results.append(news_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "login error!")
            return HttpResponseRedirect('/login')

    categories = Category.objects.filter(status='True')
    context = {
        'categories': categories,
    }
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            current_user = request.user
            data = UserProfile()
            data.user = current_user
            data.image = "images/users/default.png"
            data.save()
            messages.success(request, "Congratulations! you successfully signed up ")
            return HttpResponseRedirect('/')
        else:
            return HttpResponse("wtf")
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'signup.html', context)


def find_subs(category):
    news = []
    #for x in News.objects.filter(category_id=category.id, status='True'):
    #    news.append(x)
    if category.get_children():
        sub_categories = category.get_children()
        for rs in sub_categories:
            for n in find_subs(rs):
                news.append(n)
        return news
    else:
        return News.objects.filter(category_id=category.id, status='True')


def faq(request):
    categories = Category.objects.all()
    faqs = FAQ.objects.all().order_by('ordernumber')
    context = {
        'categories': categories,
        'faqs': faqs,
        'page': 'faq',
    }
    return render(request, 'faq.html', context)
