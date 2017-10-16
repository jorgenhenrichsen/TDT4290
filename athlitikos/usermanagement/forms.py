from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(max_length=547)

    CHOICES = (('1', 'Admin',), ('2', 'Klubbansvarlig',))
    status = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'status']
