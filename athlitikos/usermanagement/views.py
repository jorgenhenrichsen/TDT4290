from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def club_official_options(request):

    # html = ''
    return HttpResponse()


@login_required(login_url='/login')
def admin(request):
    return render(request, 'admin.html')
