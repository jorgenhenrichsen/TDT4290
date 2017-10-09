from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from .forms import LifterForm, JudgeForm, StaffForm, MoveAttemptForm, ResultForm, GroupForm, ClubForm, CompetitonForm
# from django.views.generic import UpdateView
from django.http import JsonResponse
from .models import Lifter, Judge, Staff, Result, MoveAttempt, Competition, Club

# Create your views here.


@login_required(login_url='/login')
def home(request):
    return render(request, 'resultregistration/home.html')


def lifter_detail(request, pk):
    lifter = get_object_or_404(Lifter, pk=pk)
    return render(request, 'resultregistration/lifter_detail.html',
                  {'fullname': lifter.__str__(),
                   'birth_date': lifter.birth_date.strftime('%Y-%m-%d'),
                   'gender': lifter.gender
                   })


@login_required(login_url='/login')
def add_new_lifter(request):

    if request.method == "POST":
        form = LifterForm(request.POST)
        if form.is_valid():
            lifter = form.save()
            return redirect(reverse('resultregistration:lifter_detail', args=[lifter.pk]))
    form = LifterForm()
    return render(request, 'resultregistration/edit_person.html', {'title': 'Legg til ny utøver', 'form': form})


@login_required(login_url='/login')
def add_new_judge(request):

    if request.method == "POST":
        form = JudgeForm(request.POST)
        if form.is_valid():
            judge = form.save()
            return redirect(reverse('resultregistration:judge_detail', args=[judge.pk]))
    form = JudgeForm()
    return render(request, 'resultregistration/edit_person.html', {'title': 'Legg til ny dommer', 'form': form})


def judge_detail(request, pk):
    judge = get_object_or_404(Judge, pk=pk)
    return render(request, 'resultregistration/judge_detail.html', {
        'fullname': judge.__str__(),
        'birth_date': judge.birth_date.strftime('%Y-%m-%d'),
        'level': judge.judge_level,
    })


@login_required(login_url='/login')
def add_new_staff(request):

    if request.method == "POST":
        form = StaffForm(request.POST)
        if form.is_valid():
            staff = form.save()
            return redirect(reverse('resultregistration:staff_detail', args=[staff.pk]))
    form = StaffForm()
    return render(request, 'resultregistration/edit_person.html', {'title': 'Legg til ny funksjonær', 'form': form})


def staff_detail(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    return render(request, 'staff_detail.html', {
        'fullname': staff.__str__(),
        # 'birth_date': staff.birth_date.strftime('%Y-%m-%d'),
    })



def result_registration(request):
    form = MoveAttemptForm()
    form = ResultForm()
    form = GroupForm()
    form = ClubForm()
    form = CompetitonForm()
    return render(request, 'resultregistration/resultregistration.html', context={'MoveAttemptForm': MoveAttemptForm, 'ResultForm': ResultForm, 'GroupForm': GroupForm, 'ClubForm': ClubForm, 'CompetitonForm': CompetitonForm})



def get_best_snatch_for_result(request, pk):
    all_attempts = MoveAttempt.objects.filter(parentResult=pk, moveType='Snatch')
    best_attempt = 0
    for attempt in all_attempts:
        if attempt.success and attempt.weight>best_attempt:
            best_attempt = attempt.weight
    return JsonResponse({'best_snatch': str(best_attempt)})

def get_best_clean_and_jerk_for_result(request, pk):
    all_attempts = MoveAttempt.objects.filter(parentResult=pk, moveType='Clean and jerk')
    best_attempt = 0
    for attempt in all_attempts:
        if attempt.weight > best_attempt:
            best_attempt = attempt.weight
    return JsonResponse({'best_clean_and_jerk': str(best_attempt)})


