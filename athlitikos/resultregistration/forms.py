from django import forms
from .models import InternationalResult, InternationalGroup
from .models import Competition, Club, Group, Result, MoveAttempt, Lifter, Judge, Person
from django.utils import timezone
from django.db.models import Q
from django.forms import formset_factory

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

    host = forms.ModelChoiceField(Club.objects.all())
    start_date = forms.DateField(widget=forms.DateInput(attrs={"class": "date-input", "placeholder": "mm/dd/yyyy"}))

    class Meta:
        model = Competition
        fields = ['competition_category', 'host', 'location', 'start_date']
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
        fields = '__all__'


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ['competition', 'records_description', 'competitors']
        # May have to remove the foreign key models


class GroupFormV2(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ['competition', 'competitors']

# class ResultRow(forms.):
#     pass


class MoveAttemptForm(forms.ModelForm):
    class Meta:
        model = MoveAttempt
        fields = '__all__'


class GroupFormV3(forms.Form):

    group_number = forms.IntegerField()
    competition = forms.ModelChoiceField(queryset=Competition.objects.all())
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}))
    competition_leader = forms.ModelChoiceField(queryset=Judge.objects.all(), required=False)
    jury = forms.ModelMultipleChoiceField(queryset=Judge.objects.all(), required=False)
    judges = forms.ModelMultipleChoiceField(queryset=Judge.objects.all(), required=False)
    technical_controller = forms.ModelChoiceField(queryset=Judge.objects.all(), required=False)
    chief_marshall = forms.ModelChoiceField(queryset=Judge.objects.all(), required=False)
    timekeeper = forms.ModelChoiceField(queryset=Judge.objects.all(), required=False)

    secretary = forms.CharField(required=False)
    speaker = forms.CharField(required=False)
    notes = forms.CharField(required=False)
    records_description = forms.CharField(required=False)

    def __init__(self, user, *args, **kwargs):
        super(GroupFormV3, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['competition'].queryset = Competition.objects.filter(author__exact=user)


class ResultForm(forms.Form):

    lifter = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'class': 'lifter-input-field',
               'placeholder': 'Utøver'}))
    lifter_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    club = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'class': 'club-input-field', 'placeholder': 'Klubb'}))
    club_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    birth_date = forms.DateField(widget=forms.DateInput(
        attrs={'placeholder': 'dd/mm/yyyy'}),
        input_formats=["%d/%m/%Y"])

    age_group = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={'class': 'age-group-input-field', 'placeholder': 'Aldersgruppe'}))
    weight_class = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Vektklasse'}))
    body_weight = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'kg'}))

    clean_and_jerk_1 = forms.CharField(max_length=5, widget=forms.TextInput(
        attrs={'placeholder': 'Rykk 1'}), required=False)
    clean_and_jerk_2 = forms.CharField(max_length=5, widget=forms.TextInput(
        attrs={'placeholder': 'Rykk 2'}), required=False)
    clean_and_jerk_3 = forms.CharField(max_length=5, widget=forms.TextInput(
        attrs={'placeholder': 'Rykk 3'}), required=False)

    snatch_1 = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'placeholder': 'Støt 1'}), required=False)
    snatch_2 = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'placeholder': 'Støt 2'}), required=False)
    snatch_3 = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'placeholder': 'Støt 3'}), required=False)

    def clean(self):
        cleaned_data = super(ResultForm, self).clean()

        if cleaned_data.get('lifter_id'):
            return cleaned_data
        else:
            lifter_name = cleaned_data.get('lifter')
            club = cleaned_data.get('club')

            if lifter_name and club:
                names = lifter_name.rsplit(' ', 1)
                first_name = names[0]
                last_name = names[1]
                lifter = Lifter.objects.filter(first_name__icontains=first_name,
                                               last_name__icontains=last_name,
                                               club__club_name__icontains=club).first()
                if lifter is None:
                    self.add_error('lifter', "Ingen utøver funnet!")

        return cleaned_data


class BaseResultFormSet(forms.BaseFormSet):

    def clean(self):
        if any(self.errors):
            return

        lifter_ids = []
        for form in self.forms:
            try:
                lifter_id = form.cleaned_data["lifter_id"]
            except KeyError:
                continue
            if lifter_id in lifter_ids:
                raise forms.ValidationError("Kan ikke inneholde samme utøver to ganger")
            lifter_ids.append(lifter_id)


ResultFormSet = formset_factory(ResultForm, extra=2, formset=BaseResultFormSet)


class InternationalResultForm(forms.ModelForm):
    class Meta:
        model = InternationalResult
        fields = '__all__'


class InternationalGroupForm(forms.ModelForm):
    class Meta:
        model = InternationalGroup
        fields = '__all__'


class InternationalCompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
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


class MergeLifterSearchForm(forms.Form):
    first_name = forms.CharField(label="Fornavn")
    last_name = forms.CharField(label="Etternavn")

    def clean(self, *args, **kwargs):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        lifter_qs = Lifter.objects.filter(Q(first_name__startswith=first_name) | Q(last_name__startswith=last_name))
        if not lifter_qs.count() >= 2:
            raise forms.ValidationError("Det finnes ikke flere enn to personer"
                                        " med disse søkekriterene i systemet.")

    def qs(self):
        return Lifter.objects.filter(Q(first_name__startswith=self.cleaned_data.get("first_name"))
                                     | Q(last_name__startswith=self.cleaned_data.get("last_name")))


class MergePersonCreateForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'club')

    def __init__(self, *args, **kwargs):
        super(MergePersonCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        person = super(MergePersonCreateForm, self).save(commit=False)
        if commit:
            person.save()
        return person


class MergeLifterCreateForm(forms.ModelForm):
    class Meta:
        model = Lifter
        fields = ('first_name', 'last_name', 'club', 'birth_date', 'gender')

    def __init__(self, *args, **kwargs):
        super(MergeLifterCreateForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget = forms.widgets.SelectDateWidget(years=YEAR_CHOICES)

    def save(self, commit=True):
        lifter = super(MergeLifterCreateForm, self).save(commit=False)
        if commit:
            lifter.save()
        return lifter


class ChangeResultForm(forms.ModelForm):

    class Meta:
        model = Result
        exclude = ['group', 'lifter']
