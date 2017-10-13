from django.shortcuts import render, HttpResponse
from resultregistration.models import Club, Result, Lifter
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
import json
import functools
import operator
import athlitikos.settings as settings


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
        results = search_for_results(lifter_id, club_id)
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

        lifters = search_for_lifter_containing(query)

        results = []
        for lifter in lifters:
            lifter_json = {
                'label': lifter.lifter.first_name + " " + lifter.lifter.last_name + ", " + lifter.club.club_name,
                'value': lifter.lifter.first_name + " " + lifter.lifter.last_name + ", " + lifter.club.club_name,
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
        clubs = search_for_club_containing(query)

        results = []
        for club in clubs:
            club_json = {
                'label': club.club_name,
                'value': club.club_name,
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


# HELPERS


def search_for_results(lifter_id, club_id):

    if settings.DEBUG:
        print("Searching with lifter_id={}, club_id={}".format(lifter_id, club_id))

    results = Result.objects.all()

    if lifter_id is not None and not lifter_id == 'undefined':
        results = results.filter(lifter_id__exact=lifter_id)

    if club_id is not None and not club_id == 'undefined':
        results = results.filter(lifter__club_id__exact=club_id)

    if settings.DEBUG:
        print(results)

    return results


def search_for_lifters_psql(query):
    queries = [SearchQuery(x) for x in query.split(' ')]
    vector = SearchVector('first_name', 'last_name')
    combined_queries = functools.reduce(operator.or_, queries)

    lifters = Lifter.objects.annotate(
        rank=SearchRank(vector, combined_queries)).order_by('-rank')
    lifters = lifters.filter(rank__gte=0.04)
    return lifters


def search_for_lifter_containing(query):
    lifters_first_name = Lifter.objects.filter(first_name__icontains=query)
    lifters_last_name = Lifter.objects.filter(last_name__icontains=query)
    lifters = lifters_first_name.union(lifters_last_name)
    return lifters


def search_for_club_containing(query):
    return Club.objects.filter(club_name__icontains=query)
