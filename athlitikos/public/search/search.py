from datetime import datetime
import athlitikos.settings as settings
from resultregistration.models import Club, Result, Lifter

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
    def search_for_results(cls, lifters=None, clubs=None, from_date=None, to_date=None, categories=None):
        """
        Filter out results.
        :param lifters: Only inlcude results from the lifters ids in this list.
        :param clubs: Only include results with lifters belonging to a club in this list.
        :param from_date: Only include results that has a competition start_date that are after or equal to this date.
        :param to_date: Only include results that has a competition start_date that are before or equal to this date.
        :param categories: Dictionary of categories to include results from. Form: {"age":age, "gender":gender, "weight_class":weight_class}
        :return: The filtered results.
        """

        if settings.DEBUG:
            print("Searching with lifters={}, clubs={}, from_date={}, to_date={}, categories={}"
                  .format(lifters, clubs, from_date, to_date, categories))

        results = Result.objects.all()

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
                age = category["age"]
                gender = category["gender"]
                weight_class = int(category["weight_class"])

                part_result = results.filter(age__exact=age,
                                             lifter__gender__exact=gender,
                                             weight_class__exact=weight_class
                                             )

                all_results.append(part_result)

            if len(all_results) > 1:
                end_result = all_results[0]

                for i in range(1, len(all_results)):
                    end_result = (end_result | all_results[i]).distinct()

            else:
                results = all_results[0]

        if settings.DEBUG:
            print(results)

        return results

    @classmethod
    def search_for_lifter_containing(cls, query):
        """
        Find a lifter.
        :param query:
        :return:
        """
        lifters_first_name = Lifter.objects.filter(first_name__icontains=query)
        lifters_last_name = Lifter.objects.filter(last_name__icontains=query)
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
