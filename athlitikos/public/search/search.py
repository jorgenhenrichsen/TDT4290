from datetime import datetime
import athlitikos.settings as settings
from resultregistration.models import Club, Result, Competition, Person, OldResults
from resultregistration.enums import Status
import json


"""
Contains helpers to search for objects in the database.
"""


class SearchFiltering:

    NONE_VALUES = [
        "undefined",
        "",
        "none",
        "None",
        [],
        None
    ]

    @classmethod
    def is_none_value(cls, value) -> bool:
        """
        Checks if a query parameter is a none-value, as defined in NONE_VALUES.
        :param value:
        :return: bool, true if the input is a none-value.
        """
        return value is None or SearchFiltering.NONE_VALUES.__contains__(str(value))\
            or SearchFiltering.NONE_VALUES.__contains__(value)

    @classmethod
    def get_competitions(cls, category=None, from_date=None, to_date=None, hosts=None):
        """
        Get competitions belonging to a category.
        :param category:
        :param from_date:
        :param to_date:
        :param hosts:
        :return:
        """
        if settings.DEBUG:
            print("Getting competitions with category={} from_date={} to_date={} hosts={}"
                  .format(category, from_date, to_date, hosts))

        competitions = Competition.objects.all().order_by('-start_date')

        if not SearchFiltering.is_none_value(category) and category != "all":
            competitions = competitions.filter(competition_category__iexact=category)

        if not SearchFiltering.is_none_value(from_date):
            from_date_formatted = datetime.strptime(from_date, "%d/%m/%Y").date()
            competitions = competitions.filter(start_date__gte=from_date_formatted)

        if not SearchFiltering.is_none_value(to_date):
            to_date_formatted = datetime.strptime(to_date, "%d/%m/%Y").date()
            competitions = competitions.filter(start_date__lte=to_date_formatted)

        if not SearchFiltering.is_none_value(hosts):
            all_results = []
            for host in hosts:
                all_results.append(competitions.filter(host__icontains=host))

            if len(all_results) > 1:
                end_result = all_results[0]

                for i in range(1, len(all_results)):
                    end_result = (end_result | all_results[i]).distinct()

                competitions = end_result

            else:
                competitions = all_results[0]

        return competitions[:500]

    @classmethod
    def get_best_results(cls, results, filter_by: str="p"):
        """
        Get all the unique best results in a QuerySet with results.
        :param results: QuerySet with results
        :param filter_by: What value is considered when finding the best results. Possible values:
            - p: points
            - pv: points veteran
            - w: total weight lifted
        :return:
        """

        if len(results) == 0:
            return results

        lifters_in_results = set()

        for result in results:
            lifters_in_results.add(result.lifter)

        field_name = ""

        if filter_by == "p":
            field_name = "points_with_sinclair"
        elif filter_by == "pv":
            field_name = "points_with_veteran"
        else:
            field_name = "total_lift"

        lifters_results = []

        for lifter in lifters_in_results:
            lifters_results.append(results.filter(lifter_id__exact=lifter.id).latest(field_name))

        return lifters_results

    @classmethod
    def search_for_results_with_request(cls, request):
        """
        Search for result with a HTTP request.
        The request can contain the parameters: lifters, clubs, from_date, to_date and categories.
        :param request:
        :return:
        """

        lifters_json = request.GET.get('lifters')
        clubs_json = request.GET.get('clubs')
        categories_json = request.GET.get('categories')
        lifters = None
        clubs = None
        categories = None

        if lifters_json is not None:
            lifters = json.loads(lifters_json)

        if clubs_json is not None:
            clubs = json.loads(clubs_json)

        if categories_json is not None:
            categories_dict = json.loads(categories_json)
            categories = []
            for key, value in categories_dict.items():
                categories.append(value)

        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        best_results = request.GET.get('best_results')

        results = SearchFiltering.search_for_results(lifters, clubs, from_date,
                                                     to_date, categories, best_results)
        old_results = SearchFiltering.search_for_old_results(lifters, clubs, from_date,
                                                             to_date, categories, best_results)

        if type(results) is not list:
            results = list(results.all())

        if type(old_results) is not list:
            old_results = list(old_results.all())

        results.extend(old_results)
        return results

    @classmethod
    def search_for_results(cls, lifters=None, clubs=None, from_date=None, to_date=None, categories=None,
                           best_results=None):
        """
        Filter out results.
        :param lifters: Only inlcude results from the lifters ids in this list.
        :param clubs: Only include results with lifters belonging to a club in this list.
        :param from_date: Only include results that has a competition start_date that are after or equal to this date.
        :param to_date: Only include results that has a competition start_date that are before or equal to this date.
        :param categories: Dictionary of categories to include results from.
                           Form: {"age":age, "gender":gender, "weight_class":weight_class}
        :param best_results: If this is given, only the best results according to this value is included.
        :return: The filtered results.
        """

        if settings.DEBUG:
            print("Searching with lifters={}, clubs={}, from_date={}, to_date={}, categories={}, best_results={}"
                  .format(lifters, clubs, from_date, to_date, categories, best_results))

        results = Result.objects.all().filter(group__status__exact=Status.approved.value)

        if not SearchFiltering.is_none_value(lifters):
            results = results.filter(lifter_id__in=lifters)

        if not SearchFiltering.is_none_value(clubs):
            results = results.filter(lifter__club_id__in=clubs)

        if not SearchFiltering.is_none_value(from_date):
            from_date_formatted = datetime.strptime(from_date, "%d/%m/%Y").date()
            results = results.filter(group__date__gte=from_date_formatted)

        if not SearchFiltering.is_none_value(to_date):
            to_date_formatted = datetime.strptime(to_date, "%d/%m/%Y").date()
            results = results.filter(group__date__lte=to_date_formatted)

        if not SearchFiltering.is_none_value(categories):

            all_results = []

            for category in categories:
                age_group = category["age_group"]
                gender = category["gender"]
                weight_class = int(category["weight_class"])

                part_result = results.filter(age_group__exact=age_group,
                                             lifter__gender__exact=gender,
                                             weight_class__exact=weight_class
                                             )

                all_results.append(part_result)

            if len(all_results) > 1:
                end_result = all_results[0]

                for i in range(1, len(all_results)):
                    end_result = (end_result | all_results[i]).distinct()

                results = end_result

            else:
                results = all_results[0]

        if not SearchFiltering.is_none_value(best_results):
            results = SearchFiltering.get_best_results(results, filter_by=best_results)

        if settings.DEBUG:
            print("NEW RESULTS:", results)

        return results

    @classmethod
    def search_for_old_results(cls, lifters=None, clubs=None, from_date=None,
                               to_date=None, categories=None, best_results=None):

        if settings.DEBUG:
            print("Searching for old results with"
                  " lifters={}, clubs={}, from_date={}, to_date={}, categories={}, best_results={}"
                  .format(lifters, clubs, from_date, to_date, categories, best_results))

        results = OldResults.objects.all().order_by('-competition__start_date')

        if not SearchFiltering.is_none_value(lifters):
            results = results.filter(lifter_id__in=lifters)

        if not SearchFiltering.is_none_value(clubs):
            results = results.filter(lifter__club_id__in=clubs)

        if not SearchFiltering.is_none_value(from_date):
            from_date_formatted = datetime.strptime(from_date, "%d/%m/%Y").date()
            results = results.filter(competition__start_date__gte=from_date_formatted)

        if not SearchFiltering.is_none_value(to_date):
            to_date_formatted = datetime.strptime(to_date, "%d/%m/%Y").date()
            results = results.filter(competition__start_date__lte=to_date_formatted)

        if not SearchFiltering.is_none_value(categories):
            print(categories)
            all_results = []

            for category in categories:
                age_group = category["age_group"]
                weight_class = int(category["weight_class"])

                part_result = results.filter(age_group__exact=age_group,
                                             weight_class__exact=weight_class)

                all_results.append(part_result)

            if len(all_results) > 1:
                end_result = all_results[0]

                for i in range(1, len(all_results)):
                    end_result = (end_result | all_results[i]).distinct()

                results = end_result

            else:
                results = all_results[0]

        if not SearchFiltering.is_none_value(best_results):
            print("Searching for best OLD RESTULTS")
            results = SearchFiltering.get_best_results(results, filter_by=best_results)

        if settings.DEBUG:
            print("OLD RESULTS:", results[:500])

        return results[:500]

    @classmethod
    def search_for_old_results_with_request(cls, request):

        lifters_json = request.GET.get('lifters')
        clubs_json = request.GET.get('clubs')
        categories_json = request.GET.get('categories')
        lifters = None
        clubs = None
        categories = None

        if lifters_json is not None:
            lifters = json.loads(lifters_json)

        if clubs_json is not None:
            clubs = json.loads(clubs_json)

        if categories_json is not None:
            categories_dict = json.loads(categories_json)
            categories = []
            for key, value in categories_dict.items():
                categories.append(value)

        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        best_results = request.GET.get('best_results')

        return SearchFiltering.search_for_old_results(lifters, clubs, from_date, to_date, categories, best_results)

    @classmethod
    def search_for_lifter_containing(cls, query):
        """
        Find a lifter.
        :param query:
        :return:
        """

        first_name = None
        last_name = None

        query_splitted = query.rsplit(" ", 1)
        print(query_splitted)
        if len(query_splitted) > 1:
            first_name = query_splitted[0]
            last_name = query_splitted[1]
        elif len(query_splitted) == 1:
            first_name = query_splitted[0]

        lifters = None

        if not SearchFiltering.is_none_value(first_name) and not SearchFiltering.is_none_value(last_name):
            lifters_first_last_name = Person.objects.filter(first_name__iexact=first_name,
                                                            last_name__istartswith=last_name)
            lifters_middlename = Person.objects.filter(first_name__istartswith=query)
            lifters = lifters_first_last_name.union(lifters_middlename)

        elif not SearchFiltering.is_none_value(first_name):
            lifters_first_name = Person.objects.filter(first_name__istartswith=first_name)
            lifters_last_name = Person.objects.filter(last_name__istartswith=first_name)
            lifters = lifters_first_name.union(lifters_last_name)

        return lifters

    @classmethod
    def search_for_club_containing(cls, query):
        """
        Find clubs
        :param query: The query
        :return: The clubs where the club name contains the query string.
        """
        return Club.objects.filter(club_name__icontains=query)
