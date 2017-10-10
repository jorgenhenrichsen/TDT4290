from django import forms
from .models import Lifter, Judge, Staff
from django.utils import timezone

YEAR_CHOICES = [y for y in range(1900, timezone.now().year+1)]


class LifterForm(forms.ModelForm):

    class Meta:
        model = Lifter
        fields = ('first_name', 'last_name', 'birth_date', 'gender')

    def __init__(self, *args, **kwargs):
        super(LifterForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget = forms.widgets.SelectDateWidget(years=YEAR_CHOICES)


class JudgeForm(forms.ModelForm):

    class Meta:
        model = Judge
        fields = ('first_name', 'last_name', 'birth_date', 'judge_level')

    def __init__(self, *args, **kwargs):
        super(JudgeForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget = forms.widgets.SelectDateWidget(years=YEAR_CHOICES)


class StaffForm(forms.ModelForm):

    class Meta:
        model = Staff
        fields = ('first_name', 'last_name', 'birth_date')

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget = forms.widgets.SelectDateWidget(years=YEAR_CHOICES)
