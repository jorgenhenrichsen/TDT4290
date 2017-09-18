from django import forms
from .models import Lifter


class LifterForm(forms.ModelForm):

    class Meta:
        model = Lifter
        fields = ('first_name', 'last_name', 'birth_date')
