from django.shortcuts import render, HttpResponse
import json
from .search.search import SearchFiltering
import athlitikos.settings as settings


def search(request):
    """
    The search page
    :param request:
    :return:
    """
    if request.method == 'GET' and request.is_ajax():
        lifter_id = request.GET.get('lifter_id')
        club_id = request.GET.get('club_id')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        results = SearchFiltering.search_for_results(lifter_id, club_id, from_date, to_date)

        return render(request, 'public/result-table.html', {'results': results})

    return render(request, 'public/search.html')


def search_for_lifter(request):
    """
    Used for autompletion on lifter names
    :param request:
    :return:
    """

    if request.is_ajax():
        query = request.GET.get('term', '')

        lifters = SearchFiltering.search_for_lifter_containing(query)

        results = []
        for lifter in lifters:

            lifter_string = lifter.lifter.first_name +\
                            " " + lifter.lifter.last_name +\
                            ", " + lifter.club.clubName

            lifter_json = {
                'label': lifter_string,
                'value': lifter_string,
                'id': lifter.lifter.id,
            }

            results.append(lifter_json)

        data = json.dumps(results)

    else:
        data = 'error'

    if settings.DEBUG:
        print(data)

    mime_type = 'application/json'
    return HttpResponse(data, mime_type)


def search_for_clubs(request):
    """
    Used for autompletion on club names
    :param request:
    :return:
    """
    if request.is_ajax():
        query = request.GET.get('term', '')
        clubs = SearchFiltering.search_for_club_containing(query)

        results = []
        for club in clubs:
            club_json = {
                'label': club.clubName,
                'value': club.clubName,
                'id': club.id,
            }
            results.append(club_json)

        data = json.dumps(results)

    else:
        data = 'error'

    if settings.DEBUG:
        print(data)

    mime_type = 'application/json'
    return HttpResponse(data, mime_type)
