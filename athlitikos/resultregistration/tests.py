from django.test import TestCase
from .models import Competition, Club
from .validators import validate_name


class CompetitionTestCase(TestCase):

    def setUp(self):

        Competition.objects.create(competition_category = "Norgesmesterskap", location = "Bodø", start_date = "2018-10-05")
        Competition.objects.create(competition_category = "Midtnorsk", location = "Trondheim", start_date = "2019-11-06")
        Club.objects.create(club_name="TrondheimIL", region="Trondheim", address="Arne Bergsgårds Veg 30")


    def test_competition_naming_is_valid(self):

        """Competitions with valid naming are identified by using the validate_name method"""

        norgesmesterskap = Competition.objects.get(competition_category="Norgesmesterskap")

        self.assertEqual(validate_name(norgesmesterskap.competition_category), "Norgesmesterskap")
        self.assertEqual(validate_name(norgesmesterskap.location), "Bodø")

    def test_if_one_club_can_join_many_competitions(self):

        """Two competitions are added to a club, to test that the many-to-many relationship works in the database"""


        norgesmesterskap = Competition.objects.get(competition_category = "Norgesmesterskap")
        midtnorsk = Competition.objects.get(competition_category = "Midtnorsk")
        trondheim_il = Club.objects.get(club_name = "TrondheimIL")


        trondheim_il.competition.add(norgesmesterskap, midtnorsk)

        # Checking for club names, which contain the competition Norgesmesterskap

        club_name = Club.objects.filter(competition__competition_category = "Norgesmesterskap")\
            .values_list('club_name', flat=True).first()

        self.assertEqual(club_name, "TrondheimIL")
