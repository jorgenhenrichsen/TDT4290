from django.test import TestCase
from .models import Competition, Club
from .validators import validate_name
from django.test import Client

class CompetitionTestCase(TestCase):

    def setUp(self):

        Competition.objects.create(competitionCategory = "Norgesmesterskap", location = "Bodø", startDate = "2018-10-05")
        Competition.objects.create(competitionCategory = "Midtnorsk", location = "Trondheim", startDate = "2019-11-06")
        Club.objects.create(clubName="TrondheimIL", region="Trondheim", address="Arne Bergsgårds Veg 30")

    def test_competition_naming_is_valid(self):

        """Competitions with valid naming are identified by using the validate_name method"""

        norgesmesterskap = Competition.objects.get(competitionCategory="Norgesmesterskap")

        self.assertEqual(validate_name(norgesmesterskap.competitionCategory), "Norgesmesterskap")
        self.assertEqual(validate_name(norgesmesterskap.location), "Bodø")

    def test_if_one_club_can_join_many_competitions(self):

        """Two competitions are added to a club, to test that the many-to-many relationship works in the database"""

        norgesmesterskap = Competition.objects.get(competitionCategory = "Norgesmesterskap")
        midtnorsk = Competition.objects.get(competitionCategory = "Midtnorsk")
        trondheimIL = Club.objects.get(clubName = "TrondheimIL")

        trondheimIL.competition.add(norgesmesterskap, midtnorsk)

        #Checking for club names, which contain the competition Norgesmesterskap

        club_name = Club.objects.filter(competition__competitionCategory = "Norgesmesterskap")\
            .values_list('clubName', flat=True).first()

        self.assertEqual(club_name, "TrondheimIL")












