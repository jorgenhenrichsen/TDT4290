from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import ClubOfficial
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def admin(request):
    return render(request, 'admin.html')
