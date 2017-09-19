from django import forms
from .models import Lifter
from django.utils import timezone


class LifterForm(forms.ModelForm):

    YEAR_CHOICES = [y for y in range(1900, timezone.now().year)]

    class Meta:
        model = Lifter
        fields = ('first_name', 'last_name', 'birth_date')

    def __init__(self, *args, **kwargs):
        super(LifterForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget = forms.widgets.SelectDateWidget(years=self.YEAR_CHOICES)
