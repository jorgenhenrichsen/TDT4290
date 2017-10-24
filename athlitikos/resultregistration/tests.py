from django.test import TestCase, RequestFactory
from .models import Competition, Club
from .validators import validate_name
from .views import home
from django.contrib.auth.models import User, Group
from .views import home, list_all_judges


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


class HomeTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        admin_group = Group.objects.create(name='Admin')
        club_group = Group.objects.create(name='ClubOfficial')

        self.admin = User.objects.create(username="admin")
        self.admin.groups.add(admin_group)

        self.club_ofc = User.objects.create(username="club_ofc")
        self.club_ofc.groups.add(club_group)

    def test_home_routing_to_admin(self):
        request = self.factory.get('home')
        request.user = self.admin
        response = home(request)
        self.assertEqual(response.status_code, 200, "Failed to get /home/ for admin user")

    def test_home_routing_to_club_official(self):
        request = self.factory.get('home')
        request.user = self.club_ofc
        response = home(request)
        self.assertEqual(response.status_code, 200, "Failed to get /home/ for club official user")


class JudgeTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="user")

    def test_judge_list_view_response(self):
        request = self.factory.get('judges')
        request.user = self.user
        response = list_all_judges(request)
        self.assertEqual(response.status_code, 200, "Failed to get /judges/")
