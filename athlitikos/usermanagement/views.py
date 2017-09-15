from django.shortcuts import render

# Create your views here.


# TODO: This view should be login-only
def home(request):
    return render(request, 'registration/home.html')