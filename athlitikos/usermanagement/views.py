from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import ClubOfficial

def club_official_options(request):

    html = ''
    return HttpResponse()

def admin(request):
    return render(request, 'admin.html')
