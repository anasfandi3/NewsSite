from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from home.models import UserProfile
from news.models import Category


def index(request):

    categories = Category.objects.all()
    profile = UserProfile.objects.get(user=request.user)
    context = {
        'categories': categories,
        'profile': profile,
        'page': 'Profile',

    }
    return render(request, 'user_profile.html', context)
