from django.test import TestCase
from .models import Competition, Club
from .validators import validate_name


class CompetitionTestCase(TestCase):

    def setUp(self):

        Competition.objects.create(competition_category="Norgesmesterskap", location="Bodø", start_date="2018-10-05")
        Competition.objects.create(competition_category="Midtnorsk", location="Trondheim", start_date="2019-11-06")
        Club.objects.create(club_name="TrondheimIL", region="Trondheim", address="Arne Bergsgårds Veg 30")

    def test_competition_naming_is_valid(self):

        """Competitions with valid naming are identified by using the validate_name method"""

        norgesmesterskap = Competition.objects.get(competition_category="Norgesmesterskap")

        self.assertEqual(validate_name(norgesmesterskap.competition_category), "Norgesmesterskap")
        self.assertEqual(validate_name(norgesmesterskap.location), "Bodø")
