from django.shortcuts import render, HttpResponse
from resultregistration.models import Club, Result, Lifter
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
import json
import functools
import operator


# Create your views here.

def search(request):
    """
    The search page
    :param request:
    :return:
    """
    clubs = Club.objects.all()
    if request.method == 'GET':
        query_text = request.GET.get('query_text')
        lifter_id = request.GET.get('lifter_id')

        results = search_for_results(lifter_id)

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
                'label': lifter.lifter.first_name + " " + lifter.lifter.last_name,
                'value': lifter.lifter.first_name + " " + lifter.lifter.last_name,
                'id': lifter.lifter.id,
            }
            results.append(lifter_json)

        data = json.dumps(results)

    else:
        data = 'error'

    print(data)

    mime_type = 'application/json'
    return HttpResponse(data, mime_type)

# HELPERS


def search_for_results(lifter_id):
    results = Result.objects.filter(lifter_id__exact=lifter_id)
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
