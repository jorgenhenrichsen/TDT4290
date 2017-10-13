from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserForm(forms.ModelForm):

    epost = forms.EmailField(max_length=254)
    passord = forms.CharField(widget=forms.PasswordInput)
    status = forms.CharField(max_length=254)

    class Meta:
        model = User
        fields = ['epost', 'passord', 'status']

class SignUpForm(UserCreationForm):

    epost = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ['epost', 'username']