from django import forms
from .models import Competition, Club, Group, Result, MoveAttempt, Lifter, Judge, Staff
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


# For the resultregistration page
class CompetitonForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = '__all__'
    def add_competition_if_not_exists(self):

        competition = self.cleaned_data

        competition_category = competition.get('competition_category'),
        start_date = competition.get('start_date'),
        location = competition.get('location')
        print(Competition.objects.filter(competition_category=competition_category,
                                          start_date=start_date,
                                          location=location))
        if not Competition.objects.filter(competition_category=competition_category,
                                          start_date=start_date,
                                          location=location):
            Competition.objects.create(competition_category=competition_category,
                                       start_date=start_date,
                                       location=location)
            print('yey object created')
            return competition
        else:
            print('neyy, object exists')

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ('club_name',)


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ['competition', 'records_description', 'competitors']
        # May have to remove the foreign key models


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = '__all__'
        # https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/#selecting-the-fields-to-use

# class ResultRow(forms.):
#     pass

class MoveAttemptForm(forms.ModelForm):
    class Meta:
        model = MoveAttempt
        fields = '__all__'
