from django import forms
from .models import Lifter, Judge, Staff, Result, MoveAttempt, Group, Competition, Club
from django.utils import timezone



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
        fields = ('first_name', 'last_name', 'judge_level')  # 'birth_date',

    def __init__(self, *args, **kwargs):
        super(JudgeForm, self).__init__(*args, **kwargs)
        # self.fields['birth_date'].widget = forms.widgets.SelectDateWidget(years=YEAR_CHOICES)


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ('first_name', 'last_name')  # , 'birth_date'

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)


#For the resultregistration page
class CompetitonForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = '__all__'


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ('clubName',)

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ['competition', 'recordsDescription', 'competitors']


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        exclude = ['resultID']



class MoveAttemptForm(forms.ModelForm):
    class Meta:
        model = MoveAttempt
        fields = '__all__'

