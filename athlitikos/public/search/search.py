from datetime import datetime
import athlitikos.settings as settings
from resultregistration.models import Club, Result, Lifter


def search_for_results(lifter_id, club_id, from_date, to_date):
    """
    Filter out results.
    :param lifter_id: Only inlcude results with this lifter
    :param club_id: Only include results with lifters belonging to this club
    :param from_date: Only include results that has a competition start_date that are after or equal to this date.
    :param to_date: Only include results that has a competition start_date that are before or equal to this date.
    :return: The filtered results.
    """

    if settings.DEBUG:
        print("Searching with lifter_id={}, club_id={}, from_date{}, to_date{}".format(lifter_id, club_id, from_date,
                                                                                       to_date))

    results = Result.objects.all()

    if lifter_id is not None and not lifter_id == 'undefined':
        results = results.filter(lifter_id__exact=lifter_id)

    if club_id is not None and not club_id == 'undefined':
        results = results.filter(lifter__club_id__exact=club_id)

    if from_date is not None and not from_date == 'undefined':
        from_date_formatted = datetime.strptime(from_date, "%d/%m/%Y").date()
        results = results.filter(group__competition__startDate__gte=from_date_formatted)

    if to_date is not None and not to_date == 'undefined':
        to_date_formatted = datetime.strptime(to_date, "%d/%m/%Y").date()
        results = results.filter(group__competition__startDate__lte=to_date_formatted)

    if settings.DEBUG:
        print(results)

    return results


def search_for_lifter_containing(query):
    lifters_first_name = Lifter.objects.filter(first_name__icontains=query)
    lifters_last_name = Lifter.objects.filter(last_name__icontains=query)
    lifters = lifters_first_name.union(lifters_last_name)
    return lifters


def search_for_club_containing(query):
    return Club.objects.filter(clubName__icontains=query)
