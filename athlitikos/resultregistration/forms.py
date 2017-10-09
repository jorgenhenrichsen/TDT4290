from django import forms
from .models import Lifter, Judge, Staff, Result, MoveAttempt, Group, Competition
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
        # self.fields['birth_date'].widget = forms.widgets.SelectDateWidget(years=YEAR_CHOICES)

class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ('competitionCategory', 'location', 'startDate')

    def __init__(self, *args, **kwargs):
        super(CompetitionForm, self).__init__(*args, **kwargs)


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ResultForm, self).__init__(*args, **kwargs)


class MoveAttemptForm(forms.ModelForm):
    class Meta:
        model = MoveAttempt
        fields = ('parentResult', 'moveType', 'attemptNum', 'weight', 'success')

    def __init__(self, *args, **kwargs):
        super(MoveAttemptForm, self).__init__(*args, **kwargs)
