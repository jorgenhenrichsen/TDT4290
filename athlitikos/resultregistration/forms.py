from django import forms
from .models import Competition, Club, Group, Result, MoveAttempt, Lifter, Judge
from django.utils import timezone

YEAR_CHOICES = [y for y in range(1900, timezone.now().year+1)]


class LifterForm(forms.ModelForm):
    class Meta:
        model = Lifter
        fields = ('first_name', 'last_name', 'birth_date', 'gender', 'club')

    def __init__(self, *args, **kwargs):
        super(LifterForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget = forms.widgets.SelectDateWidget(years=YEAR_CHOICES)


class JudgeForm(forms.ModelForm):
    class Meta:
        model = Judge
        fields = ('first_name', 'last_name', 'judge_level', 'club')  # 'birth_date',

    def __init__(self, *args, **kwargs):
        super(JudgeForm, self).__init__(*args, **kwargs)
        # self.fields['birth_date'].widget = forms.widgets.SelectDateWidget(years=YEAR_CHOICES)


# For the resultregistration page
class CompetitonForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = '__all__'
    # def add_competition_if_not_exists(self):
    #
    #     competition = self.cleaned_data
    #
    #     competition_category = competition.get('competition_category'),
    #     start_date = competition.get('start_date'),
    #     location = competition.get('location')
    #     print(Competition.objects.filter(competition_category=competition_category,
    #                                       start_date=start_date,
    #                                       location=location))
    #     if not Competition.objects.filter(competition_category=competition_category,
    #                                       start_date=start_date,
    #                                       location=location):
    #         Competition.objects.create(competition_category=competition_category,
    #                                    start_date=start_date,
    #                                    location=location)
    #         print('yey object created')
    #         return competition
    #     else:
    #         print('neyy, object exists')


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ('club_name',)


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ['competition', 'records_description', 'competitors']
        # May have to remove the foreign key models


class GroupFormV2(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ['competition', 'competitors']


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


class PendingResultForm(forms.Form):
    weight_class = forms.CharField(max_length=3)
    body_weight = forms.FloatField()
    category = forms.CharField(max_length=4)

    birth_date = forms.DateField()
    lifter_first_name = forms.CharField(max_length=200)
    lifter_last_name = forms.CharField(max_length=200)
    club = forms.CharField(max_length=200)

    snatch1 = forms.CharField(max_length=5)
    snatch2 = forms.CharField(max_length=5)
    snatch3 = forms.CharField(max_length=5)

    clean_and_jerk1 = forms.CharField(max_length=5)
    clean_and_jerk2 = forms.CharField(max_length=5)
    clean_and_jerk3 = forms.CharField(max_length=5)

    best_snatch = forms.CharField(max_length=4, required=False)
    best_clean_and_jerk = forms.CharField(max_length=4, required=False)
    total = forms.CharField(max_length=5, required=False)
    points = forms.CharField(max_length=6, required=False)
    veteran_points = forms.CharField(max_length=6, required=False)
    pl = forms.CharField(max_length=6, required=False)
    rekord = forms.CharField(max_length=8, required=False)
    sinclair_coefficient = forms.CharField(max_length=9, required=False)
