from django import forms
from .models import *
from django.utils import timezone
from betterforms.multiform import MultiModelForm


YEAR_CHOICES = [y for y in range(1900, timezone.now().year)]


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


# For the resultregistration page
class CompetitonForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = '__all__'


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = '__all__'

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        # May have to remove the foreign key models

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        exclude = ['resultID']
        # https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/#selecting-the-fields-to-use


class MoveAttemptForm(forms.ModelForm):
    class Meta:
        model = MoveAttempt
        fields = '__all__'

class CompiledResultRegistrationForm(MultiModelForm):
    form_classes = {
        'competition-details': CompetitonForm,
        'administrative-details': GroupForm,
        'lifter': LifterForm,
        'move-attempt': MoveAttemptForm,
        'results': ResultForm,
    }