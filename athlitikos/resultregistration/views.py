from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from .forms import LifterForm, JudgeForm
from .models import Lifter, Judge

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
    return render(request, 'edit_person.html', {'title': 'Legg til ny utøver', 'form': form})


@login_required(login_url='/login')
def add_new_judge(request):

    if request.method == "POST":
        form = JudgeForm(request.POST)
        if form.is_valid():
            judge = form.save()
            return redirect(reverse('resultregistration:judge_detail', args=[judge.pk]))
    form = JudgeForm()
    return render(request, 'edit_person.html', {'title': 'Legg til ny dommer', 'form': form})


def judge_detail(request, pk):
    judge = get_object_or_404(Judge, pk=pk)
    return render(request, 'judge_detail.html', {
        'fullname': judge.__str__(),
        'birth_date': judge.birth_date.strftime('%Y-%m-%d'),
        'level': judge.judge_level,
    })


@login_required(login_url='/login')
def add_new_staff(request, pk):
    pass


def staff_detail(request, pk):
    pass
