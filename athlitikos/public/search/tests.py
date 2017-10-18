from django.test import TestCase
from .search import SearchFiltering
from resultregistration.models import Result, Lifter, Club, Group, Competition, Judge
from resultregistration.enums import Status

class SearchFilteringTestCase(TestCase):

    club1 = None
    club2 = None

    result1 = None
    result2 = None

    lifter1 = None
    lifter2 = None

    def setUp(self):

        staff = 'Staff Staff'

        judge = Judge.objects.create(
            first_name='Judge',
            last_name='Judge',
            judge_level=1,
        )

        self.club1 = Club.objects.create(club_name="Club1")
        self.club2 = Club.objects.create(club_name="Club2")

        competition = Competition.objects.create(
            competition_category="Category",
            start_date="2017-08-19",
            location="Location"
        )

        group = Group.objects.create(
            competition=competition,
            date="2017-08-20",
            group_number=1,
            competition_leader=staff,
            secretary=staff,
            speaker=staff,
            technical_controller=judge,
            cheif_marshall=judge,
            time_keeper=judge,
            status=Status.approved,
        )

        denied_group = Group.objects.create(
            competition=competition,
            date="2017-08-20",
            group_number=2,
            competition_leader=staff,
            secretary=staff,
            speaker=staff,
            technical_controller=judge,
            cheif_marshall=judge,
            time_keeper=judge,
            status=Status.denied,
        )

        self.lifter1 = Lifter.objects.create(
            first_name="Lifter",
            last_name="One",
            birth_date="1998-09-09",
            gender='M',
            club=self.club1,
        )

        self.lifter2 = Lifter.objects.create(
            first_name="Lifter",
            last_name="Two",
            birth_date="1990-05-01",
            gender="F",
            club=self.club2,
        )

        self.result1 = Result.objects.create(
            points_with_veteran=1000,
            points_with_sinclair=900,
            total_lift=200,
            age=40,
            sinclair_coefficient=1.1,
            veteran_coefficient=1.1,
            body_weight=70,
            age_group="M1",
            group=group,
            lifter=self.lifter1,
            weight_class=72,
        )

        self.result2 = Result.objects.create(
            points_with_veteran=1000,
            points_with_sinclair=900,
            total_lift=200,
            age=40,
            sinclair_coefficient=1.1,
            veteran_coefficient=1.1,
            body_weight=70,
            age_group="M1",
            group=group,
            lifter=self.lifter2,
            weight_class=72,
        )

        self.result3 = Result.objects.create(
            points_with_veteran=1000,
            points_with_sinclair=900,
            total_lift=200,
            age=40,
            sinclair_coefficient=1.1,
            veteran_coefficient=1.1,
            body_weight=70,
            age_group="M1",
            group=denied_group,
            lifter=self.lifter2,
            weight_class=72,
        )

    def test_value_validation(self):
        self.assertTrue(SearchFiltering.is_none_value(None))
        self.assertTrue(SearchFiltering.is_none_value("None"))
        self.assertTrue(SearchFiltering.is_none_value(""))
        self.assertTrue(SearchFiltering.is_none_value([]))
        self.assertTrue(SearchFiltering.is_none_value("undefined"))
        self.assertTrue(SearchFiltering.is_none_value("none"))

    def test_search_for_results_by_club(self):
        results = SearchFiltering.search_for_results(clubs=[self.club1.pk])
        self.assertTrue(len(results) == 1)
        self.assertTrue(self.result1 == results[0])

    def test_search_for_results_by_lifter(self):
        results = SearchFiltering.search_for_results(lifters=[self.lifter1.pk])
        self.assertTrue(len(results) == 1, "Could not fetch results for a lifter")
        self.assertTrue(self.result1 == results[0], "The result fetched for a lifter is not correct.")

    def test_search_for_results_by_multiple_clubs(self):
        results = SearchFiltering.search_for_results(clubs=[self.club1.pk, self.club2.pk])
        self.assertTrue(len(results) == 2, "Could not fetch results by mulitple club ids")

    def test_search_for_results_by_multiple_lifters(self):
        results = SearchFiltering.search_for_results(lifters=[self.lifter1.pk, self.lifter2.pk])
        self.assertTrue(len(results) == 2, "Could not fetch results by multiple lifters.")

    def test_search_for_lifters(self):
        results = SearchFiltering.search_for_lifter_containing("Lif")
        self.assertTrue(len(results) == 2)
        results = SearchFiltering.search_for_lifter_containing("One")
        self.assertTrue(len(results) == 1)

    def test_search_for_clubs(self):
        results = SearchFiltering.search_for_club_containing("1")
        self.assertTrue(len(results) == 1)
        results = SearchFiltering.search_for_club_containing("Club")
        self.assertTrue(len(results) == 2)

    def test_search_for_results_from_date(self):
        results = SearchFiltering.search_for_results(from_date="20/08/2017")
        self.assertEqual(len(results), 2)
        results = SearchFiltering.search_for_results(from_date="21/08/2017")
        self.assertEqual(len(results), 0)

    def test_search_for_results_to_date(self):
        results = SearchFiltering.search_for_results(to_date="20/08/2017")
        self.assertEqual(len(results), 2)
        results = SearchFiltering.search_for_results(to_date="19/08/2017")
        self.assertEqual(len(results), 0)

    def test_search_for_results_by_category(self):
        category = {"age_group": "M1", "gender": "M", "weight_class": "72"}
        results = SearchFiltering.search_for_results(categories=[category])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.result1)

        category = {"age_group": "M1", "gender": "F", "weight_class": "72"}
        results = SearchFiltering.search_for_results(categories=[category])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.result2)

    def test_search_for_multiple_categories(self):
        categories = [
            {"age_group": "M1", "gender": "M", "weight_class": "72"},
            {"age_group": "M1", "gender": "F", "weight_class": "72"},
        ]
        results = SearchFiltering.search_for_results(categories=categories)
        self.assertEqual(len(results), 2, "Failed to search for multiple categories")
