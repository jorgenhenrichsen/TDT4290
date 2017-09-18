from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


# TODO: This view should be login-only
@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html')


