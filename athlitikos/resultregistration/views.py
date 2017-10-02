from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from .forms import LifterForm, JudgeForm, StaffForm, ResultRegistrationForm
from .models import Lifter, Judge, Staff, Competition, Group, Result

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
        'birth_date': staff.birth_date.strftime('%Y-%m-%d'),
    })


def result_registration(request):
    form = ResultRegistrationForm()
    return render(request, 'resultregistration/resultregistration.html', {'form': form})


    # returns all the tings you need to make the result registration form
    # def build_competition_info(competition_info):
    #     return {
    #         'cateogry': group.competition.competitionCategory,
    #         'organizer': club.clubName,
    #         'location': group.competition.location,
    #         'date': group.date,
    #         'pool': group.groupNumber,
    #         'staff_leader': group.competitionLeader,
    #         'staff_jury': group.jury,
    #         'staff_secretary': group.secretary,
    #         'staff_speaker': group.speaker,
    #         'judge_1': group.judges,
    #         'judge_2': group.judges,
    #         'judge_3': group.judges,
    #         'staff_controller': group.technicalController,
    #         'staff_chief_marshall': group.cheifMarshall,
    #         'staff_time_keeper': group.timeKeeper,
    #         'notes': group.recordsDescription,
    #     }
    # def build_competator(competator):
    #     return {
    #         # 'weightclass'
    #         # 'bodyWeight'
    #         # 'category'
    #         'birth_date': group.competitors.lifter.birth_date,
    #         'fullname': group.competitors.lifter.__str__(),
    #         'club': group.competitors.lifter.club,
    #         # 'snatch_attempt_1'
    #         # 'snatch_attempt_2'
    #         # 'snatch_attempt_3'
    #         # 'jerk_attempt_1'
    #         # 'jerk_attempt_2'
    #         # 'jerk_attempt_3'
    #         'best_snatch': result.best_snatch,
    #         'best_jerk': result.best_clean_and_jerk,
    #         'total_weight': result.total,
    #         'points': result.points,
    #         'vetaran_points': result.points_veteran,
    #         # 'placement':
    #         # 'record'
    #         # 'sinclair'
    #     }

