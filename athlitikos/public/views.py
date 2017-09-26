from django.shortcuts import render

# Create your views here.


def search(request):
    return render(request, 'public/search.html', {'clubs': ["Club 1", "Club 2"]})
