from django.test import TestCase
from .models import Competition
from .validators import validate_name
from django.core.exceptions import ValidationError

class CompetitionTestCase(TestCase):

    def setUp(self):
        Competition.objects.create(competitionCategory="Norgesmesterskap", location="Bodø", startDate = "2018-10-05")
        Competition.objects.create(competitionCategory="NM3", location="Trondheim", startDate = "2019-11-06")

    def test_competition_naming_is_valid(self):

        """Competitions with valid competition-categories are identified"""

        norgesmesterskap = Competition.objects.get(competitionCategory="Norgesmesterskap")

        self.assertEqual(validate_name(norgesmesterskap.competitionCategory), "Norgesmesterskap")

