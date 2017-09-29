from django.shortcuts import render
from resultregistration.models import Club, Result
from django.contrib.postgres.search import SearchVector

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
