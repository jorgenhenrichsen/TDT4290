from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from .forms import LifterForm
from .models import Lifter

# Create your views here.


# TODO: This view should be login-only
@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html')


def lifter_detail(request, pk):
    lifter = get_object_or_404(Lifter, pk=pk)
    return render(request, 'lifter_detail.html',
                  {'fullname': lifter.__str__(),
                   'birth_date': lifter.birth_date.strftime('%Y-%m-%d')
                   })


@login_required(login_url='/login')
def add_new_lifter(request):

    if request.method == "POST":
        form = LifterForm(request.POST)
        if form.is_valid():
            lifter = form.save()
            return redirect(reverse('resultregistration:lifter_detail', args=[lifter.pk]))
    form = LifterForm()
    return render(request, 'edit_lifter.html', {'form': form})

