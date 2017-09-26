from django.shortcuts import render
from athlitikos.resultregistration.models import Lifter

def autocomplete(request):
    return render(request, 'base.html')

def search_club_names(request):

    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''

    #clubs = Club.objects.filter()

