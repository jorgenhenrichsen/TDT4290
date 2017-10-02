import sys

from django.views.decorators.csrf import csrf_exempt
from .models import Person
from django.shortcuts import render

@csrf_exempt
def autocomplete(request):
    print("JEG ER HER", file=sys.stderr)

    language = 'en-us'
    session_language = 'en-us'
    if 'lang' in request.COOKIES:
        language = request.COOKIES['lang']
    if 'lang' in request.session:
        session_language = request.session['lang']

    args = {}
  #  args.update(csrf(request)) (check into csrf-protection)
    args['articles'] = Person.objects.all()
    args['language'] = language
    args['session_language'] = session_language

    return render(request, 'autocomplete/base.html', args)

@csrf_exempt
def search_person_names(request):
    print("JEG ER HER TO", file=sys.stderr)
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ""

    persons = Person.objects.filter(first_name__contains=search_text)

    return render(request, 'autocomplete/ajax_search.html', {'persons' : persons})

