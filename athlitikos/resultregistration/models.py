from django.db import models
from .enums import Gender, JudgeLevel, MoveTypes, AgeGroup
from math import log10
from datetime import date
from .enums import Gender, JudgeLevel
from .validators import validate_name
#from datetime import datetime
#from django.db.models.signals import pre_save is usefull ;)


# Create your models here.

class Competition(models.Model):
    # comeptitionArranger = models.ForeignKey(Organisation)
    competitionCategory = models.CharField(max_length=100,validators=[validate_name])
    location = models.CharField(max_length=100)
    startDate = models.DateField(help_text="år-måned-dag")

    def __str__(self):
        return '{0}, {1}, {2}'.format(self.competitionCategory, self.location, self.startDate)

class Club(models.Model):
    clubName = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    models.ManyToManyField(Competition, null=True) #One Club can join many competitions

    def __str__(self):
        return self.clubName


class Group(models.Model):
    #   Identifying
    groupNumber = models.IntegerField()
    competition = models.ForeignKey(Competition)
    date = models.DateField()

    competitors = models.ManyToManyField('Lifter')

    competitionLeader = models.ForeignKey('Staff', related_name='competitionLeader')
    jury = models.ManyToManyField('Staff', related_name='jury')
    judges = models.ManyToManyField('Judge', related_name='judges')
    secretary = models.ForeignKey('Staff', related_name='secretary')
    speaker = models.ForeignKey('Staff', related_name='speaker')
    technicalController = models.ForeignKey('Staff', related_name='technicalController')
    cheifMarshall = models.ForeignKey('Staff', related_name='chiefMarshall')
    timeKeeper = models.ForeignKey('Staff', related_name='timeKeeper')

    notes = models.CharField(max_length=300, null=True, blank=True)
    recordsDescription = models.CharField(max_length=300,  null=True, blank=True)

    def __str__(self):
        return '{0}, group {1}, {2}'.format(self.competition, self.groupNumber, self.date)

    class Meta:
        unique_together = ('groupNumber', 'competition')

# Result for weightlifting(snatch/cleanAndJerk)
class Result(models.Model):

    def populate_age_coefficients(self, file_path):
        valueFile = open(file_path)
        values = valueFile.read()
        valuelist = []
        coeffs = {}
        for l in values.split('\n'):
            valuelist += l.split()
        for i in range(0,len(valuelist),2):
            coeffs[valuelist[i]] = valuelist[i+1]
        return coeffs

    def populate_sinclair_coeff(self, file_path):
        sinclairFile = open(file_path)
        values = sinclairFile.read()
        valuelist = []
        for l in values.split('\n'):
            valuelist += l.split()
        sinclairAMan = float(valuelist[-4])
        sinclairAWoman = float(valuelist[-3])
        sinclairbMan = float(valuelist[-2])
        sinclairbWoman = float(valuelist[-1])
        return sinclairAMan, sinclairAWoman, sinclairbMan, sinclairbWoman


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.melzer_faber = self.populate_age_coefficients(file_path='/athlitikos/static/athlitikos/coefficients/meltzerFaberCoefficients.txt')
    #     self.sinclair_A_men, self.sinclair_b_men, self.sinclair_A_women, self.sinclair_b_women = self.populate_sinclair_coeff(file_path='../athlitikos/static/athlitikos/coefficients/sinclairValues.txt')


    melzer_faber = {}
    sinclair_A_men = 0
    sinclair_b_men = 0
    sinclair_A_women = 0
    sinclair_b_women = 0

    resultID = models.IntegerField(primary_key=True)
    group = models.ForeignKey(Group, null=True)     # The Group that this result belongs to.
    lifter = models.ForeignKey('Lifter', null=True)    # The Lifter that this result belongs to
    body_weight = models.FloatField(verbose_name='Kroppsvekt', null=True)
    age_group = models.CharField(max_length=20, verbose_name='Kategori', choices=AgeGroup.choices(), null=True)

    _sinclair_coefficient = models.FloatField(db_column='sinclair_coefficient', null=True, blank=True)
    # _best_clean_and_jerk = models.ForeignKey('MoveAttempt', related_name='best_clean_and_jerk', db_column='best_clean_and_jerk', null=True, blank=True)
    # _best_snatch = models.ForeignKey('MoveAttempt', related_name='best_snatch', db_column='best_snatch', null=True, blank=True)

    def get_age(self):
        if self.lifter:
            lifter = Lifter.objects.get(pk=self.lifter)
            return date.today().year - lifter.birth_date.year
        return 0
    age = 0
    # age = date.today().year - lifter.birth_date.year

    # @property
    # def weight_class(self):
    weight_class = models.IntegerField(verbose_name='Vektklasse', null=True)

    # @property
    # def sinclair_coefficient(self):
    #     return self._sinclair_coefficient

    # @sinclair_coefficient.setter
    @property
    def sinclair_coefficient(self):
        if self.lifter.gender == 'M': # or decimalField?
            a = self.sinclair_A_men
            b = self.sinclair_b_men
        else: #self.lifter.gender == 'K':
            a = self.sinclair_A_women
            b = self.sinclair_b_women
        if self.body_weight > b:
            self._sinclair_coefficient = 1
        else:
            x = log10(self.body_weight/b)
            self._sinclair_coefficient = 10**(a*(x**2))
        return self._sinclair_coefficient



    @property
    def points(self):
        return self.get_best_snatch.weight + self.get_best_clean_and_jerk.weight

    #   points multiplied with sinclair coefficient
    @property
    def total(self):
        return self.points*self.sinclair_coefficient

    @property
    def veteranTotal(self):

        if self.age not in self.melzer_faber:
            return self.total
        else:
            return self.total*self.melzer_faber[self.age]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.melzer_faber \
            = self.populate_age_coefficients('D:/Projects/TDT4290/athlitikos/athlitikos/static/athlitikos/coefficients/meltzerFaberCoefficients.txt')  #(BASE_DIR + '/static/athlitikos/coefficients/meltzerFaberCoefficients.txt')
        self.sinclair_A_men, self.sinclair_b_men, self.sinclair_A_women, self.sinclair_b_women\
            = self.populate_sinclair_coeff('D:/Projects/TDT4290/athlitikos/athlitikos/static/athlitikos/coefficients/sinclairValues.txt')
        self.age = self.get_age()

    def __str__(self):
        return self.lifter.fullname() + str(self.group.competition)







class MoveAttempt(models.Model):
    # Currently only made for the lifting attempts, not the pentathlon

    parentResult = models.ForeignKey('Result', on_delete=models.CASCADE)    # The Result this is part of
    moveType = models.CharField(max_length=20, choices=MoveTypes.choices())
    attemptNum = models.IntegerField()
    weight = models.IntegerField()  # Weight that was attempted lifted
    success = models.BooleanField()

    def __str__(self):
        return '{0}, attempt {1}, weight {2}, {3}'.format(self.moveType, self.attemptNum, self.weight, self.success)

    class Meta:
        # The MoveAttempt should be uniquely identified
        # by a combination of the result it belongs to, the attempt number and the moveType
        unique_together = ('parentResult', 'attemptNum', 'moveType')


class Person(models.Model):
    first_name = models.CharField(max_length=40, verbose_name='Fornavn', validators=[validate_name])
    last_name = models.CharField(max_length=100, verbose_name='Etternavn', validators=[validate_name])

    def __str__(self):
        return self.fullname()

    def fullname(self):
        return "{} {}".format(self.first_name, self.last_name)


class Lifter(Person):

    birth_date = models.DateField(verbose_name='Fødselsdato', null=True)   # Changed from dateTime, as we don't need time of birth
    gender = models.CharField(max_length=10, verbose_name='Kjønn', choices=Gender.choices(), null=True)
    club = models.ForeignKey('Club', null=True)  # The club that this lifter< belongs to


class Judge(Person):

    judge_level = models.CharField(max_length=10, choices=JudgeLevel.choices(), default=JudgeLevel.Level0)




class Staff(Person):
    pass

class Sinclair_coefficients(models.Model):
    gender = models.CharField(max_length=10, verbose_name='Kjønn', choices=Gender.choices())
    body_weight = models.DecimalField(verbose_name='Kroppsvekt',max_digits=4,decimal_places=1)
    coefficient = models.FloatField(verbose_name='Sinclairkoeffisient')

    class Meta:
        unique_together = ('gender', 'body_weight', 'coefficient')
