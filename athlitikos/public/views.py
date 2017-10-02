from django.shortcuts import render, HttpResponse
from resultregistration.models import Club, Result, Lifter
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.views.decorators.csrf import csrf_exempt
import json
import functools
import operator


# Create your views here.


def search(request):

    clubs = Club.objects.all()
    if request.method == 'GET':
        query_text = request.GET.get('query_text')

        results = Result.objects.annotate(
            search=SearchVector('lifter__first_name', 'lifter__last_name')
        ).filter(search=query_text)

        return render(request, 'public/search.html', {'clubs': clubs, 'results': results})

    return render(request, 'public/search.html', {'clubs': clubs})


@csrf_exempt
def search_for_lifter(request):

    if True:#request.is_ajax():
        terms = request.GET.get('term', '')
        print(terms)
        # `search` is the user's provided search string.
        queries = [SearchQuery(query) for query in terms.split(' ')]
        print(queries)
        # `name` is where the name of the school is stored in the model.
        vector = SearchVector('first_name', 'last_name')
        query = functools.reduce(operator.or_, queries)

        lifters = Lifter.objects.annotate(
            rank=SearchRank(vector, query)).order_by('-rank')
        lifters = lifters.filter(rank__gte=0.04)

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


