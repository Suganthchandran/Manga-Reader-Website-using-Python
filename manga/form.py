from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'user-input'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'user-input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'user-input'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'user-input'}))
    
    class Meta:
        model = User
        fields = ['username','email', 'password1','password2']
