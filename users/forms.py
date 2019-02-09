from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
        labels = {
            'email': 'Email',
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
        }


class ProfileRegisterForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['internal_user_id', 'position', 'team', 'localization']
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': '+48123456789'})
        }