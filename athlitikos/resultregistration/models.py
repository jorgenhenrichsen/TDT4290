from django.db import models
from .enums import MoveTypes, AgeGroup, Gender, JudgeLevel, Status, CompetitionCategory
from .validators import validate_name
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
# from datetime import datetime
# from django.db.models.signals import pre_save is usefull ;)
from django.contrib.auth import get_user_model
User = get_user_model()


class MelzerFaber(models.Model):
    age = models.IntegerField(verbose_name='Alder')
    coefficient = models.FloatField(verbose_name='Koeffisient')
    year = models.IntegerField(verbose_name='Årstall')

    class Meta:
        unique_together = ('age', 'coefficient', 'year')

    def __str__(self):
        return 'M-F for år {}: {}:{}'.format(self.year, self.age, self.coefficient)


class Sinclair(models.Model):
    gender = models.CharField(max_length=10, verbose_name='Kjønn', choices=Gender.choices())
    sinclair_b = models.FloatField(verbose_name='b')
    sinclair_A = models.FloatField(verbose_name='A')
    year = models.IntegerField(verbose_name='Årstall')

    class Meta:
        unique_together = ('gender', 'sinclair_b', 'sinclair_A', 'year')

    def __str__(self):
        return


class Competition(models.Model):

    competition_category = models.CharField(max_length=100,
                                            choices=CompetitionCategory.choices(),
                                            verbose_name="Kategori")

    host = models.CharField(max_length=100, verbose_name="Arrangør")
    location = models.CharField(max_length=100)
    start_date = models.DateField(help_text="år-måned-dag")

    def __str__(self):
        return '{0}, {1}, {2}'.format(self.competition_category, self.location, self.start_date)


class Club(models.Model):
    club_name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.club_name


class Group(models.Model):
    #   Identifying attributes
    group_number = models.IntegerField()
    competition = models.ForeignKey(Competition)
    date = models.DateField()

    status = models.CharField(max_length=30, default=Status.not_sent, choices=Status.choices(), null=False)

    competitors = models.ManyToManyField('Lifter')

    competition_leader = models.ForeignKey('Judge',
                                           verbose_name='Stevneleder',
                                           related_name="groups_competition_leader")
    # , related_name='competition_leader')
    jury = models.ManyToManyField('Judge', verbose_name='Jurie', default='', related_name='groups_juries')
    judges = models.ManyToManyField('Judge', related_name='groups_judges')
    secretary = models.CharField(max_length=100, verbose_name='Sekretær')  # , related_name='secretary')
    speaker = models.CharField(max_length=100, verbose_name='Taler')  # , related_name='speaker')

    technical_controller = models.ForeignKey('Judge', verbose_name='Teknisk kontrollør',
                                             related_name='groups_technical_controller')
    cheif_marshall = models.ForeignKey('Judge', verbose_name='Chief Marshall', related_name='groups_chief_marshall')
    time_keeper = models.ForeignKey('Judge', verbose_name='Tidtaker', related_name='groups_time_keeper')

    notes = models.CharField(max_length=300, null=True, blank=True)
    records_description = models.CharField(max_length=300, null=True, blank=True)

    author = models.ForeignKey(User, null=True)

    def __str__(self):
        return '{0}, gruppe {1}, {2}'.format(self.competition, self.group_number, self.date)

    class Meta:
        unique_together = ('group_number', 'competition')


# Result for weightlifting(snatch/cleanAndJerk)
class Result(models.Model):

    # resultID = models.IntegerField(primary_key=True)    # Removed, as built in pk is better

    group = models.ForeignKey(Group, null=True)     # The Group that this result belongs to.
    lifter = models.ForeignKey('Lifter', null=True)    # The Lifter that this result belongs to
    body_weight = models.FloatField(verbose_name='Kroppsvekt', null=True)
    age_group = models.CharField(max_length=20, verbose_name='Kategori', choices=AgeGroup.choices(), null=True)
    weight_class = models.CharField(max_length=10, verbose_name='Vektklasse', null=True)

    sinclair_coefficient = models.FloatField(db_column='sinclair_coefficient', null=True, blank=True)
    veteran_coefficient = models.FloatField(db_column='melzer_faber_coefficient', null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    best_clean_and_jerk = models.ForeignKey('MoveAttempt', related_name='best_clean_and_jerk',
                                            db_column='best_clean_and_jerk', null=True, blank=True)
    best_snatch = models.ForeignKey('MoveAttempt', related_name='best_snatch',
                                    db_column='best_snatch', null=True, blank=True)

    total_lift = models.IntegerField(verbose_name='Total poeng',
                                     blank=True, null=True)  # best_clean_and_jerk + best_snatch
    points_with_sinclair = models.FloatField(verbose_name='Poeng med sinclair',
                                             blank=True, null=True)  # total_lift*sinclair_coefficient
    points_with_veteran = models.FloatField(verbose_name='Veteranpoeng',
                                            blank=True, null=True)   # points_with_sinclair*melzerfaber_coefficient

    class Meta:
        unique_together = ('group', 'lifter')

    def __str__(self):
        return 'resultat for {0} i {1}'.format(self.lifter.fullname(), str(self.group))


class MoveAttempt(models.Model):
    # Currently only made for the lifting attempts, not the pentathlon
    parent_result = models.ForeignKey('Result', on_delete=models.CASCADE)    # The Result this is part of
    move_type = models.CharField(max_length=20, choices=MoveTypes.choices())
    attempt_num = models.IntegerField(validators=[MaxValueValidator(3), MinValueValidator(1)])
    weight = models.IntegerField()  # Weight that was attempted lifted
    success = models.BooleanField()

    def __str__(self):
        return '{0}, attempt {1}, weight {2}, {3}'.format(self.move_type, self.attempt_num, self.weight, self.success)

    class Meta:
        # The MoveAttempt should be uniquely identified
        # by a combination of the result it belongs to, the attempt number and the moveType
        unique_together = ('parent_result', 'attempt_num', 'move_type')


class Person(models.Model):
    first_name = models.CharField(max_length=40, verbose_name='Fornavn', validators=[validate_name])
    last_name = models.CharField(max_length=100, verbose_name='Etternavn', validators=[validate_name])

    def __str__(self):
        return self.fullname()

    def fullname(self):
        return "{} {}".format(self.first_name, self.last_name)


class Lifter(Person):
    # Changed from dateTime, as we don't need time of birth
    birth_date = models.DateField(verbose_name='Fødselsdato', null=True)
    gender = models.CharField(max_length=10, verbose_name='Kjønn', choices=Gender.choices(), null=True)
    club = models.ForeignKey('Club', null=True)  # The club that this lifter< belongs to


class Judge(Person):

    judge_level = models.CharField(max_length=10, choices=JudgeLevel.choices(), default=JudgeLevel.kretsdommer)


class PentathlonResult(models.Model):

    lifter = models.ForeignKey(Lifter, null=True)
    competition = models.ForeignKey(Competition, null=True)

    shot_put = models.DecimalField(max_digits=10, decimal_places=5)
    shot_put_points = models.DecimalField(max_digits=10, decimal_places=5)
    forty_meter = models.DecimalField(max_digits=10, decimal_places=5)
    forty_meter_points = models.DecimalField(max_digits=10, decimal_places=5)
    jump = models.DecimalField(max_digits=10, decimal_places=5)
    jump_points = models.DecimalField(max_digits=10, decimal_places=5)
    sum_all = models.DecimalField(max_digits=10, decimal_places=5)

    def __str__(self):
        return "Fem-kamp resultat til: " + "{} {}".format(self.lifter.first_name, self.lifter.last_name)


class Staff(Person):
    pass
