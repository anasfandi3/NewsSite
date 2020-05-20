from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

from home.models import Setting, ContactFormMessage, ContactForm
from news.models import News, Category


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = News.objects.all()[:3]
    categories = Category.objects.all()
    context = {'setting': setting,
               'sliderdata': sliderdata,
               'categories': categories,
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
    context = {'setting': setting, 'page': 'contact'}
    return render(request, 'contact.html', context)

