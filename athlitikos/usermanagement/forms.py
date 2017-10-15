from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(max_length=547)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class SignUpForm(UserCreationForm):

    epost = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ['epost', 'username']