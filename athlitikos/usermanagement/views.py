from django.shortcuts import render, redirect
from .forms import LifterForm
# Create your views here.


# TODO: This view should be login-only
def home(request):
    return render(request, 'registration/home.html')


def add_new_lifter(request):

    if request.method == "POST":
        form = LifterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = LifterForm()
        return render(request, 'registration/edit_lifter.html', {'form': form})