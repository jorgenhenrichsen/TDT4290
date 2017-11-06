from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from resultregistration.utils import parse_judge, parse_judges
from .models import Judge, Group
from .models import PentathlonResult, InternationalGroup
from django.db.models import Q
from .models import InternationalResult
from .forms import InternationalResultForm, InternationalGroupForm
from .forms import InternationalCompetitionForm
from .models import Result
from .forms import LifterForm, JudgeForm, MoveAttemptForm, ClubForm
from .forms import ResultForm, ResultFormSet, GroupFormV3
from resultregistration.models import Lifter
import json
from .resultparser import resultparser, resultserializer
from .enums import Status
from .forms import CompetitonForm, GroupFormV2, ChangeResultForm, PendingResultForm,\
    MergeLifterSearchForm, MergeLifterCreateForm
from .excel import read_competition_staff, read_lifters, read_competition_details, readexcel
from django.contrib import messages
from django.core import exceptions


def v2_result_registration(request):

    if request.method == "POST":
        r_formset = ResultFormSet(request.POST, request.FILES)
        group_form = GroupFormV3(user=request.user, data=request.POST)
        resultparser.parse_result(group_form=group_form, result_formset=r_formset, user=request.user)
    else:
        r_formset = ResultFormSet()
        group_form = GroupFormV3(user=request.user)
    return render(request,
                  "resultregistration/resultregistration_v2.html",
                  {'result_formset': r_formset, 'group_form': group_form})


@login_required(login_url='/login')
def v2_edit_result(request, pk):

    group = get_object_or_404(Group, pk=pk)
    group_data, results_data = resultserializer.serialize_group(group)

    if request.method == "POST":
        r_formset = ResultFormSet(request.POST, request.FILES)
        group_form = GroupFormV3(user=request.user, data=request.POST)
        resultparser.parse_result(group_form=group_form, result_formset=r_formset, user=request.user)
        messages.success(request, "Resultat lagret!")
    else:
        group_form = GroupFormV3(user=request.user, initial=group_data)
        r_formset = ResultFormSet(initial=results_data)

    return render(request, "resultregistration/resultregistration_v2.html",
                  {'result_formset': r_formset, 'group_form': group_form})


def get_result_autofill_data(request):
    """
    Used for autofilling data when user selects lifter in the resultregistration form.
    :param request:
    :return:
    """
    lifter_id = request.GET.get('lifter_id')
    lifter = get_object_or_404(Lifter, pk=lifter_id)

    data = {
        "club": {
            "name": lifter.club.club_name,
            "id": lifter.club.id,
        },
        "birth_date": lifter.birth_date.strftime('%d/%m/%Y')
    }

    json_data = json.dumps(data)
    mime_type = "application/json"
    return HttpResponse(json_data, mime_type)


@login_required(login_url='/login')
def add_new_competition(request):

    if request.method == "POST":
        form = CompetitonForm(request.POST)
        if form.is_valid():
            competition = form.save()
            competition.author = request.user
            competition.save()
            messages.success(request, "Konkurranse lagret!")
    else:
        form = CompetitonForm()
    return render(request, "resultregistration/competition_form.html", {"title": "Nytt stevne", "form": form})


@login_required(login_url='/login')
def home(request):
    if request.user.is_club_admin or request.user.is_staff:
        return home_admin(request)
    else:
        return home_club_official(request)


@login_required(login_url='/login')
def home_admin(request):
    groups = Group.objects.filter(status__in=[Status.approved.value, Status.denied.value, Status.pending.value])\
        .union(Group.objects.filter(author__exact=request.user))

    return render(request, 'resultregistration/home_admin.html', {'pending_groups': groups})


@login_required(login_url='/login')
def home_club_official(request):
    groups = Group.objects.filter(author=request.user)
    return render(request, 'resultregistration/home_club_official.html', {'pending_groups': groups})


def lifter_detail(request, pk):
    lifter = get_object_or_404(Lifter, pk=pk)
    return render(request, 'resultregistration/lifter_detail.html',
                  {'fullname': lifter.__str__(),
                   'birth_date': lifter.birth_date.strftime('%Y-%m-%d'),
                   'gender': lifter.gender,
                   'club': lifter.club,
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
def add_new_club(request):

    if request.method == "POST":
        form = ClubForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('resultregistration:home_admin'))
    form = ClubForm()
    return render(request, 'resultregistration/edit_person.html', {'title': 'Legg til ny klubb', 'form': form})


@login_required(login_url='/login')
def add_new_internationalresult(request):

    if request.method == "POST":
        form = InternationalResultForm(request.POST)
        if form.is_valid():
            international_result = form.save()
            print(international_result)
            return redirect(reverse('resultregistration:international_result_detail',
                                    args=[international_result.pk]))

    form = InternationalResultForm()
    return render(request, 'resultregistration/new_international_result.html',
                  {'title': 'Legg til nytt internasjonalt resultat', 'form': form})


@login_required(login_url='/login')
def merge_find_two_lifters_view(request, *args, **kwargs):

    if not request.user.is_club_admin and not request.user.is_staff:  # hvis man ikke request ikke har rettigheter
        return HttpResponseRedirect('/home')

    searchform = MergeLifterSearchForm(request.POST or None)
    lifter_qs = None
    if searchform.is_valid():
        lifter_qs = searchform.qs()
    context = {'searchform': searchform, 'lifter_qs': lifter_qs}
    return render(request, 'resultregistration/merge_lifters.html', context)


@login_required(login_url='/login')
def merge_lifter_view(request, *args, **kwargs):

    if not request.user.is_club_admin and not request.user.is_staff:  # hvis man ikke request ikke har rettigheter
        return HttpResponseRedirect('/home')

    # alle utøvere har en personid, som de arver fra superklassen.
    if request.POST.get('ny') is not None:
        personidlist = request.POST.getlist('ny')  # en ekstremt kreativ måte å sende over fra template tilbake til view
    else:
        personidlist = request.POST.getlist("valgt")

    lifter_qs = Lifter.objects.filter(pk__in=personidlist)
    print(lifter_qs.count())
    if lifter_qs.count() != 2:
        return HttpResponseRedirect("/merge-lifters/", messages.error(request, 'velg kun 2 personer'))
    form = MergeLifterCreateForm(request.POST or None)
    if form.is_valid():
        # Should have a try-cach block like all code working with a database ;)
        try:
            lifter_obj = form.save()
            lifter_obj1 = lifter_qs.first()
            lifter_obj2 = lifter_qs.last()

            result_qs = Result.objects.filter(Q(lifter=lifter_obj1) | Q(lifter=lifter_obj2))

            for result in result_qs:
                result.lifter = lifter_obj
                result.save()

            pent_qs = PentathlonResult.objects.filter(Q(lifter=lifter_obj1) | Q(lifter=lifter_obj2))
            for pent_result in pent_qs:
                pent_result.lifter = lifter_obj
                pent_result.save()

            group_qs1 = Group.objects.filter(Q(competitors=lifter_obj1))
            for group in group_qs1:
                group.competitors.remove(lifter_obj1)
                group.competitors.add(lifter_obj)
                group.save()

            group_qs2 = Group.objects.filter(Q(competitors=lifter_obj2))

            for group in group_qs2:
                group.competitors.remove(lifter_obj2)
                group.competitors.add(lifter_obj)
                group.save()

            igroup_qs1 = InternationalGroup.objects.filter(Q(competitors=lifter_obj1))
            for igroup in igroup_qs1:
                igroup.competitors.remove(lifter_obj1)
                igroup.competitors.add(lifter_obj)
                igroup.save()

            igroup_qs2 = InternationalGroup.filter(Q(competitors=lifter_obj2))

            for igroup in igroup_qs2:
                igroup.competitors.remove(lifter_obj2)
                igroup.competitors.add(lifter_obj)
                igroup.save()

            lifter_obj1.delete()
            lifter_obj2.delete()
            return HttpResponseRedirect("/home/admin", messages.success(request, 'utøvere slått sammen'))
        except exceptions.FieldDoesNotExist or exceptions.ObjectDoesNotExist:
            return HttpResponseRedirect("/merge-lifters/",
                                        messages.error(request, 'en eller flere utøvere har ikke resultat.'))

    return render(request, 'resultregistration/merging_lifters.html', {'form': form, 'personidlist': personidlist})


@login_required(login_url='/login')
def add_new_staff(request):
    return request


@login_required(login_url='/login')
def add_new_international_group(request):

    if request.method == "POST":
        form = InternationalGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('resultregistration:add_new_internationalresult')

    form = InternationalGroupForm()
    return render(request, 'resultregistration/new_international_group.html',
                  {'title': 'Legg til ny internasjonal pulje', 'form': form})


@login_required(login_url='/login')
def add_new_international_competition(request):

    if request.method == "POST":
        form = InternationalCompetitionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('resultregistration:add_new_internationalresult')

    form = InternationalCompetitionForm()
    return render(request, 'resultregistration/new_international_competition.html',
                  {'title': 'Legg til ny internasjonal konkurranse', 'form': form})


def international_result_detail(request, pk):

    international_result = get_object_or_404(InternationalResult, pk=pk)

    return render(request, 'resultregistration/international_result_detail.html',
                  context={'lifter': international_result.__str__(),
                           'body_weight': international_result.body_weight,
                           'age_group': international_result.age_group,
                           'weight_class': international_result.weight_class,
                           'sinclair_coefficient': international_result.sinclair_coefficient,
                           'veteran_coefficient': international_result.veteran_coefficient,
                           'age': international_result.age,
                           'best_clean_and_jerk': international_result.best_clean_and_jerk,
                           'best_snatch': international_result.best_snatch,
                           'total_lift': international_result.total_lift,
                           'points_with_sinclair': international_result.points_with_sinclair,
                           'points_with_veteran': international_result.points_with_veteran})


def judge_detail(request, pk):
    judge = get_object_or_404(Judge, pk=pk)
    return render(request, 'resultregistration/judge_detail.html', {
        'fullname': judge.__str__(),
        # 'level': judge.judge_level,
        'level': judge.get_judge_level_display,
        'club': judge.club,
    })


@login_required(login_url='/login')
def list_all_judges(request):
    list_of_judges = Judge.objects.all()
    judgelist = []
    for judge in list_of_judges:
        entry = {'judge': judge}
        # entry['judge'] = judge
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


def result_view(request):
    # form = forms.M
    row_id = request.POST.get('row_id')
    return render(request, 'resultregistration/result_form.html',
                  context={'ResultForm': ResultForm,
                           'LifterForm': LifterForm,
                           'PendingForm': PendingResultForm,
                           'row_id': row_id})


def group_registration(request):
    return render(request, 'resultregistration/group_form.html', context={'GroupForm': GroupFormV2})


def result_registration(request):
    if not request.user.is_club_admin and not request.user.is_staff:  # hvis man ikke request ikke har rettigheter
        return HttpResponseRedirect('/home')
    # result_form = ResultForm.

    return render(request, 'resultregistration/resultregistration.html', context={'MoveAttemptForm': MoveAttemptForm,
                                                                                  'ResultForm': ResultForm,
                                                                                  'PendingForm': PendingResultForm,
                                                                                  'LifterForm': LifterForm,
                                                                                  'GroupForm': GroupFormV2,
                                                                                  'ClubForm': ClubForm,
                                                                                  'CompetitonForm': CompetitonForm,
                                                                                  'indexes':
                                                                                      [1, 2, 3, 4, 5, 6, 7, 8, 9,
                                                                                       10, 11, 12, 13, 14, 15, 16,
                                                                                       17, 18]})


@login_required(login_url='/login')
def edit_result(request, pk):
    if not request.user.is_club_admin and not request.user.is_staff:  # hvis man ikke request ikke har rettigheter
        return HttpResponseRedirect('/home')
    group = Group.objects.filter(pk=pk)
    results = Result.objects.filter(group=group)
    context = {
        'pending_results': results,
        'groups': group
    }

    return render(request, 'resultregistration/editresult.html', context)


@login_required(login_url='/login')
def edit_result_clubofc(request, pk):
    if not request.user.is_club_admin and not request.user.is_staff:  # hvis man ikke request ikke har rettigheter
        return HttpResponseRedirect('/home')
    group = Group.objects.filter(pk=pk)
    results = Result.objects.filter(group=group)
    context = {
        'pending_results': results,
        'groups': group
    }

    return render(request, 'resultregistration/editresult_clubofc.html', context)


@login_required(login_url='/login')
def approve_group(request, pk):
    if not request.user.is_club_admin and not request.user.is_staff:  # hvis man ikke request ikke har rettigheter
        return HttpResponseRedirect('/home')
    group = Group.objects.get(pk=pk)
    group.status = Status.approved.value
    group.save()
    return redirect('/home/')


@login_required(login_url='/login')
def reject_group(request, pk):
    if not request.user.is_club_admin and not request.user.is_staff:  # hvis man ikke request ikke har rettigheter
        return HttpResponseRedirect('/home')
    group = Group.objects.get(pk=pk)
    group.status = Status.denied.value
    group.save()
    return redirect('/home/')


@login_required(login_url='/login')
def send_group(request, pk):
    group = Group.objects.get(pk=pk)
    group.status = Status.pending.value
    group.save()
    return redirect('/home/')


def delete_group(request, pk):
    group = Group.objects.get(pk=pk)
    results = Result.objects.filter(group=group)
    group.delete()
    results.delete()
    return redirect('/home/')


@login_required(login_url='/login')
def change_result(request, pk):
    if not request.user.is_club_admin and not request.user.is_staff:  # hvis man ikke request ikke har rettigheter
        return HttpResponseRedirect('/home')
    changing_result = Result.objects.get(pk=pk)
    group_result_belongs_to = changing_result.group
    group_primary_key = group_result_belongs_to.pk

    if request.method == "POST":
        form = ChangeResultForm(request.POST)
        if form.is_valid():

            data = form.cleaned_data

            changing_result.body_weight = data['body_weight']
            changing_result.age_group = data['age_group']
            changing_result.weight_class = data['weight_class']
            changing_result.sinclair_coefficient = data['sinclair_coefficient']
            changing_result.veteran_coefficient = data['veteran_coefficient']
            changing_result.age = data['age']
            changing_result.best_clean_and_jerk = data['best_clean_and_jerk']
            changing_result.best_snatch = data['best_snatch']
            changing_result.total_lift = data['total_lift']
            changing_result.points_with_sinclair = data['points_with_sinclair']
            changing_result.points_with_veteran = data['points_with_veteran']

            changing_result.save()

            return redirect(reverse('resultregistration:edit_result', args=[group_primary_key]))

    initial_form_values = {'body_weight': changing_result.body_weight,
                           'age_group': changing_result.age_group,
                           'weight_class': changing_result.weight_class,
                           'sinclair_coefficient': changing_result.sinclair_coefficient,
                           'veteran_coefficient': changing_result.veteran_coefficient,
                           'age': changing_result.veteran_coefficient,
                           'best_clean_and_jerk': changing_result.best_clean_and_jerk,
                           'best_snatch': changing_result.best_snatch,
                           'total_lift': changing_result.total_lift,
                           'points_with_sinclair': changing_result.points_with_sinclair,
                           'points_with_veteran': changing_result.points_with_veteran}

    form = ChangeResultForm(initial=initial_form_values)

    return render(request, 'resultregistration/edit_person.html', {'title': 'Endre valgt resultat', 'form': form})


@login_required(login_url='/login')
def change_result_clubofc(request, pk):

    changing_result = Result.objects.get(pk=pk)
    group_result_belongs_to = changing_result.group
    group_primary_key = group_result_belongs_to.pk

    if request.method == "POST":
        form = ChangeResultForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            changing_result.body_weight = data['body_weight']
            changing_result.age_group = data['age_group']
            changing_result.weight_class = data['weight_class']
            changing_result.sinclair_coefficient = data['sinclair_coefficient']
            changing_result.veteran_coefficient = data['veteran_coefficient']
            changing_result.age = data['age']
            changing_result.best_clean_and_jerk = data['best_clean_and_jerk']
            changing_result.best_snatch = data['best_snatch']
            changing_result.total_lift = data['total_lift']
            changing_result.points_with_sinclair = data['points_with_sinclair']
            changing_result.points_with_veteran = data['points_with_veteran']

            changing_result.save()
            return redirect(reverse('resultregistration:edit_result_clubofc', args=[group_primary_key]))

    initial_form_values = {'body_weight': changing_result.body_weight,
                           'age_group': changing_result.age_group,
                           'weight_class': changing_result.weight_class,
                           'sinclair_coefficient': changing_result.sinclair_coefficient,
                           'veteran_coefficient': changing_result.veteran_coefficient,
                           'age': changing_result.veteran_coefficient,
                           'best_clean_and_jerk': changing_result.best_clean_and_jerk,
                           'best_snatch': changing_result.best_snatch,
                           'total_lift': changing_result.total_lift,
                           'points_with_sinclair': changing_result.points_with_sinclair,
                           'points_with_veteran': changing_result.points_with_veteran}

    form = ChangeResultForm(initial=initial_form_values)

    return render(request, 'resultregistration/edit_person.html', {'title': 'Endre valgt resultat', 'form': form})


@login_required(login_url='/login')
def result_from_excel(request):
    if request.method == 'POST':
        success = False
        if not request.FILES:
            r_formset = ResultFormSet(request.POST, request.FILES)
            print("request.post:", request.POST)
            print('request.FILES', request.FILES)
            group_form = GroupFormV3(user=request.user, data=request.POST)
            resultparser.parse_result(group_form=group_form, result_formset=r_formset, user=request.user)
        else:
            excel_file = request.FILES['excel_file']
            try:
                data = readexcel(excel_file)
                competition_details = read_competition_details(data)
                result_details = read_lifters(data)
                results = []
                for i in range(len(result_details)):
                    row = result_details[i]
                    lifter_id = None
                    club_id = None

                    result_row = {
                        'lifter': row[4],
                        'lifter_id': lifter_id,
                        'club': row[5],
                        'club_id': club_id,
                        'birth_date': row[3],
                        'age_group': row[2],
                        'weight_class': row[0],
                        'body_weight': row[1],
                        # 'start_number': row[4],
                        'snatch_1': row[6],
                        'snatch_2': row[7],
                        'snatch_3': row[8],
                        'clean_and_jerk_1': row[9],
                        'clean_and_jerk_2': row[10],
                        'clean_and_jerk_3': row[11],
                        # # 'key': key
                    }
                    # results.update(result_row)
                    results.append(result_row)
                group_details = read_competition_staff(data)
                # print(group_details)
                # print(competition_details)

                # competition_leader_error = parse_judge(group_details['competition_leader'])

                group_details['group_number'] = competition_details[4]
                group_details['date'] = competition_details[3]
                group_details['competition_leader'] = parse_judge(group_details['competition_leader'])
                group_details['time_keeper'] = parse_judge(group_details['time_keeper'])
                group_details['judges'] = parse_judges(group_details['judges'])
                group_details['jury'] = parse_judges(group_details['jury'])

                success = True

                r_formset = ResultFormSet(initial=results)
                group_form = GroupFormV3(user=request.user, initial=group_details)
                # group_form.add_error('competition_leader', competition_leader_error)
                # resultparser.parse_result(group_form=group_form, result_formset=r_formset, user=request.user)
                # print("should be success")
                # print("r_formset:\n---\n")
                # print(str(r_formset))
                # print("group_form:\n---\n", group_form)
                return render(request,
                              'resultregistration/resultregistration_v2.html',
                              {'result_formset': r_formset, 'group_form': group_form})
                # redirect('resultregistration:result_registration_with_excel', context={'result_formset': r_formset,
                # 'group_form': group_form})
            except IOError:
                response = {
                    'success': success,
                    'error': 'File invalid or not found'
                }

            return render(request, 'resultregistration/resultregistration_v2.html', context=response)
        return render(request,
                      "resultregistration/resultregistration_v2.html",
                      {'result_formset': r_formset, 'group_form': group_form})
    else:
        return render(request, 'resultregistration/import_excel.html')

    # return render(request, 'resultregistration/resultregistration.html', context={'success': True})
