from django.shortcuts import render, HttpResponse
import json
from .search import SearchFiltering
import athlitikos.settings as settings
from resultregistration.models import Club, Result, Lifter


def search(request):
    """
    The search page
    :param request:
    :return:
    """

    clubs = Club.objects.all()
    if request.method == 'GET':
        lifter_id = request.GET.get('lifter_id')
        club_id = request.GET.get('club_id')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        results = SearchFiltering.search_for_results(lifter_id, club_id, from_date, to_date)

        return render(request, 'public/search.html', {'clubs': clubs, 'results': results})

    return render(request, 'public/search.html', {'clubs': clubs})


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
            lifter_json = {
                'label': lifter.lifter.first_name + " " + lifter.lifter.last_name + ", " + lifter.club.clubName,
                'value': lifter.lifter.first_name + " " + lifter.lifter.last_name + ", " + lifter.club.clubName,
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


def search_for_results(request):

    if request.is_ajax():
        data = 'some'
    else:
        data = 'error'

    mime_type = 'application/json'
    return HttpResponse(data, mime_type)


