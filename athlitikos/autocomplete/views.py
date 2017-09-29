from django.shortcuts import render
from .models import Person
#from django.middleware.csrf import Cs
from django.shortcuts import render_to_response

def autocomplete(request):
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

    return render_to_response('autocomplete/base.html', args)

def search_person_names(request):

    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''

    persons = Person.objects.filter(name__contains = search_text)

    return render_to_response('ajax_search.html', {'persons' : persons})

