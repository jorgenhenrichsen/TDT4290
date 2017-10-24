from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import date
from .models import Lifter, Judge, Staff, Result, MoveAttempt, Group, InternationalResult
from .forms import LifterForm, JudgeForm, StaffForm, MoveAttemptForm, ResultForm, GroupForm, ClubForm, CompetitonForm, \
    InternationalResultForm


@login_required(login_url='/login')
def home(request):
    groups = Group.objects.filter(author=request.user)
    return render(request, 'resultregistration/home.html', {'pending_groups': groups})


@login_required(login_url='/login')
def home_admin(request):
    return render(request, 'resultregistration/home_admin.html')


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


@login_required(login_url='/login')
def add_new_internationalresult(request):

    if request.method == "POST":
        form = InternationalResultForm(request.POST)
        if form.is_valid():
            international_result = form.save()
            return redirect(reverse('resultregistration:international_result_detail',
                                    args=[international_result.pk]))

    form = InternationalResultForm()
    return render(request, 'resultregistration/edit_person.html',
                  {'title': 'Legg til nytt internasjonalt resultat', 'form': form})



def international_result_detail(request, pk):
    international_result = get_object_or_404(InternationalResult, pk=pk)
    context = {
        'fullname': international_result.__str__(),
        'body_weight': international_result.body_weight,
        'group': international_result.group,
        'snatch': international_result.snatch,
        'clean_and_jerk': international_result.clean_and_jerk,
        'total': international_result.total
    }

    return render(request, 'resultregistration/international_result_detail.html',
                  context={'fullname': international_result.__str__(),
                            'body_weight': international_result.body_weight,
                            'group': international_result.group,
                            'snatch': international_result.snatch,
                            'clean_and_jerk': international_result.clean_and_jerk,
                            'total': international_result.total})


def judge_detail(request, pk):
    judge = get_object_or_404(Judge, pk=pk)
    return render(request, 'resultregistration/judge_detail.html', {
        'fullname': judge.__str__(),
        # 'birth_date': judge.birth_date.strftime('%Y-%m-%d'),
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
    return render(request, 'resultregistration/staff_detail.html', {
        'fullname': staff.__str__(),
        # 'birth_date': staff.birth_date.strftime('%Y-%m-%d'),
    })


@login_required(login_url='/login')
def list_all_judges(request):
    list_of_judges = Judge.objects.all()
    judgelist = []
    for judge in list_of_judges:
        entry = {}
        entry['judge'] = judge

        role_leader = judge.groups_competition_leader.all()
        role_jury = judge.groups_juries.all()
        role_judge = judge.groups_judges.all()
        role_techcontroller = judge.groups_technical_controller.all()
        role_chiefmarshall = judge.groups_chief_marshall.all()
        role_timekeeper = judge.groups_time_keeper.all()

        all_competitions = role_leader | role_jury | role_judge | \
            role_techcontroller | role_chiefmarshall | role_timekeeper

        entry['competitions'] = all_competitions.distinct()

        judgelist.append(entry)

    return render(request, 'resultregistration/judge_list.html', {'judgelist': judgelist})


def get_best_snatch_for_result(request, pk):
    all_attempts = MoveAttempt.objects.filter(parent_result=pk, move_type='Snatch')
    best_attempt = 0
    for attempt in all_attempts:
        if attempt.success and attempt.weight > best_attempt:
            best_attempt = attempt.weight
    result = Result.objects.get(pk=pk)
    result.best_snatch = best_attempt
    result.save()
    return JsonResponse({'best_snatch': str(best_attempt)})


def get_best_clean_and_jerk_for_result(request, pk):
    all_attempts = MoveAttempt.objects.filter(parent_result=pk, move_type='Clean and jerk')
    best_attempt = 0
    for attempt in all_attempts:
        if attempt.weight > best_attempt:
            best_attempt = attempt.weight
    result = Result.objects.get(pk=pk)
    result.best_clean_and_jerk = best_attempt
    result.save()
    return JsonResponse({'best_clean_and_jerk': str(best_attempt)})


def get_lift_total_for_result(request, pk):
    result = get_object_or_404(Result, pk=pk)
    best_clean_and_jerk = result.best_clean_and_jerk
    best_snatch = result.best_snatch
    total_lift = best_snatch.weight+best_clean_and_jerk.weight
    result.total_lift = total_lift
    return JsonResponse({'total_lift': str(total_lift)})


def get_points_with_sinclair_for_result(request, pk):
    result = get_object_or_404(Result, pk=pk)
    total = result.total_lift*result.sinclair_coefficient
    result.points_with_sinclair = total
    result.save()
    return JsonResponse({'points_with_sinclair': str(total)})


def get_points_with_veteran_for_result(request, pk):
    result = get_object_or_404(Result, pk=pk)
    veteran_points = result.points_with_sinclair*result.veteran_coefficient
    result.points_with_veteran = veteran_points
    result.save()
    return JsonResponse({'points_with_veteran': str(veteran_points)})


def get_age_for_lifter_in_result(request, pk):
    result = get_object_or_404(Result, pk=pk)
    age = date.today().year - result.lifter.birth_date.year
    result.age = age
    result.save()
    return JsonResponse({'age': str(age)})


def result_registration(request):
    return render(request, 'resultregistration/resultregistration.html', context={'MoveAttemptForm': MoveAttemptForm,
                                                                                  'ResultForm': ResultForm,
                                                                                  'GroupForm': GroupForm,
                                                                                  'ClubForm': ClubForm,
                                                                                  'CompetitonForm': CompetitonForm})


def edit_result(request, pk):
    group = Group.objects.filter(pk=pk)
    results = Result.objects.filter(group=group)
    context = {
        'pending_results': results,
        'groups': group
    }

    return render(request, 'resultregistration/editresult.html', context)


def approve_group(request, pk):
    group = Group.objects.get(pk=pk)
    group.status = "Godkjent"
    group.save()
    return redirect('/home/')


def reject_group(request, pk):
    group = Group.objects.get(pk=pk)
    group.status = "Ikke godkjent"
    group.save()
    return redirect('/home/')


def delete_group(request, pk):
    group = Group.objects.get(pk=pk)
    results = Result.objects.filter(group=group)
    group.delete()
    results.delete()
    return redirect('/home/')
