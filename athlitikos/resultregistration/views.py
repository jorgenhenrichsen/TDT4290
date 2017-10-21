from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from datetime import date
from .models import Lifter, Judge, Staff, Result, MoveAttempt, Group
from .forms import LifterForm, JudgeForm, StaffForm, MoveAttemptForm, ResultForm, GroupForm, ClubForm, CompetitonForm
# from django.views.generic import UpdateView


@login_required(login_url='/login')
def home(request):
    groups = Group.objects.filter(author=request.user)
    return render(request, 'resultregistration/home.html', {'pending_groups': groups})


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
    for judge in list_of_judges:
        print(judge)
        # print(judge.judge_level)
        competitionlist = []
        if Q(judge.groups_competition_leader.all().exists()) |
            competitionlist.append(judge.groups_competition_leader.all().values('competition', 'date'))
            # competitionlist.append(judge.groups_competition_leader.all())
            print('LISTEN', competitionlist)
            # for group in competitionlist:
            #     print('Competition leader i:')
            #     print(group[0]['competition'])
            #     print(group[0]['date'])
            # print('Stevneleder', judge.groups_competition_leader.all().values('competition', 'date')[0])
        if judge.groups_juries.all().exists():
            competitionlist.append(judge.groups_juries.all().values('competition', 'date'))
            # print('Jurie:', judge.groups_juries.all())
        if judge.groups_judges.all().exists():
            competitionlist.append(judge.groups_judges.all().values('competition', 'date'))
            # print('Dommer:', judge.groups_judges.all())
        if judge.groups_technical_controller.all().exists():
            competitionlist.append(judge.groups_technical_controller.all().values('competition', 'date'))
            # print('Technical controller', judge.groups_technical_controller.all())
        if judge.groups_chief_marshall.all().exists():
            competitionlist.append(judge.groups_chief_marshall.all().values('competition', 'date'))
            # print('Chief marshall', judge.groups_chief_marshall.all())
        if judge.groups_time_keeper.all().exists():
            competitionlist.append(judge.groups_time_keeper.all().values('competition', 'date'))
            # print('Time keeper', judge.groups_time_keeper.all())
            print(str(competitionlist))
        # temp = {}
        # temp['name'] =
        # temp['competitions'] =
        # hovedliste.append(temp)
        # morten_list = []


    return render(request, 'resultregistration/judge_list.html', {'judgelist': list_of_judges})

# def extract_date_time(competitionlist):
#
#     for group in competitionlist:
#         print(group[0]['competition, ''date'])
#
#     return


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
