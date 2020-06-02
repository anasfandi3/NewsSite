from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, FileInput, Select

from home.models import UserProfile


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', )
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'first name'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'last name'}),
        }


CITY = [
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('Izmir', 'Izmir'),
]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'country', 'city', 'address', 'image', )
        widgets = {
            'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'country': Select(attrs={'class': 'form-control', 'placeholder': 'country'}, choices=CITY),
            'city': TextInput(attrs={'class': 'form-control', 'placeholder': 'city'}),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'address'}),
            'image': FileInput(attrs={'class': 'form-control', 'placeholder': 'image'}),
        }