from django import forms
from .models import Lifter


class LifterForm(forms.ModelForm):

    class Meta:
        model = Lifter
        fields = ('first_name', 'last_name', 'birth_date')

    def __init__(self, *args, **kwargs):
        super(LifterForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget = forms.widgets.SelectDateWidget()
