from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LifterForm

# Create your views here.


# TODO: This view should be login-only
@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html')


# TODO: Should be login-only
def add_new_lifter(request):

    if request.method == "POST":
        form = LifterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = LifterForm()
        return render(request, 'registration/edit_lifter.html', {'form': form})