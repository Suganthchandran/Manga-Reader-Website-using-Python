# forms.py
from django import forms

class PasswordResetRequestForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
