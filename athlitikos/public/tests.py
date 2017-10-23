from django.test import TestCase, RequestFactory
from .views import search_for_lifter, search_for_clubs, search, get_available_weight_classes, get_age_groups
from resultregistration.models import Lifter, Club


class SearchTestCase(TestCase):

    def setUp(self):

        Lifter.objects.create(
            first_name="Ola",
            last_name="Nordmann",
            birth_date="1990-09-09",
        )

        Club.objects.create(
            club_name="Club",
        )

        self.factory = RequestFactory()

    def test_search(self):
        request = self.factory.get('search', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = search(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.get('search')
        response = search(request)
        self.assertEqual(response.status_code, 200)

    def test_search_lifter(self):
        request = self.factory.get('search_for_lifter', HTTP_X_REQUESTED_WITH='XMLHttpRequest', data={
            'term': 'Ola',
        })
        response = search_for_lifter(request)
        self.assertEqual(response.status_code, 200, "Error searching for lifter")

    def test_search_for_clubs(self):
        request = self.factory.get('search_for_clubs', HTTP_X_REQUESTED_WITH='XMLHttpRequest', data={
            'term': 'Clu',
        })
        response = search_for_clubs(request)
        self.assertEqual(response.status_code, 200, "Error searching for clubs")

    def test_get_age_groups(self):
        request = self.factory.get('get_age_groups', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = get_age_groups(request)
        self.assertEqual(response.status_code, 200, "Error getting age groups")

    def test_get_weight_classes(self):
        request = self.factory.get('get_available_weight_classes', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = get_available_weight_classes(request)
        self.assertEqual(response.status_code, 200, "Error getting weightclasses")
