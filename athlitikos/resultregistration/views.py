from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import FormView
from .mixins import AjaxFormMixin
from .models import Lifter, Judge, Group, Competition
from .models import PentathlonResult, InternationalGroup
from .forms import LifterForm, JudgeForm, MoveAttemptForm, ResultForm, GroupForm, ClubForm
from django.contrib import messages
from django.db.models import Q
# from .utils import *
# from .forms import PendingResultForm
# from .forms import forms
# from django.views.generic import UpdateView
from .models import InternationalResult
from .forms import InternationalResultForm, InternationalGroupForm
from .forms import InternationalCompetitionForm
from .models import Result, MoveAttempt
from .forms import CompetitonForm, GroupFormV2, ChangeResultForm, PendingResultForm,\
    MergeLifterSearchForm, MergeLifterCreateForm
from django.core import exceptions


@login_required(login_url='/login')
def home(request):
    if request.user.is_club_admin or request.user.is_staff:
        return home_admin(request)
    else:
        return home_club_official(request)


@login_required(login_url='/login')
def home_admin(request):
    groups = Group.objects.all()
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


def merge_find_two_lifters_view(request, *args, **kwargs):

    if not request.user.is_club_admin and not request.user.is_staff:  # hvis man ikke request ikke har rettigheter
        return HttpResponseRedirect('/home')

    searchform = MergeLifterSearchForm(request.POST or None)
    lifter_qs = None
    if searchform.is_valid():
        lifter_qs = searchform.qs()
    context = {'searchform': searchform, 'lifter_qs': lifter_qs}
    return render(request, 'resultregistration/merge_lifters.html', context)


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


def add_new_international_group(request):

    if request.method == "POST":
        form = InternationalGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('resultregistration:add_new_internationalresult')

    form = InternationalGroupForm()
    return render(request, 'resultregistration/new_international_group.html',
                  {'title': 'Legg til ny internasjonal pulje', 'form': form})


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


class CompetitionFormView(AjaxFormMixin, FormView):
    form_class = CompetitonForm
    template_name = 'resultregistration/competition_form.html'
    success_url = '/form-success/'

    def post(self, request, *args, **kwargs):
        competition_form = CompetitonForm(request.POST)
        # competition = self.request.POST
        # print('enters post')
        # print(competition)
        if competition_form.is_valid():
            data = competition_form.cleaned_data
            # print(competition.cleaned_data)
            print('\ncompetition valid\n', data)
            competition_category = data['competition_category']
            start_date = data['start_date']
            location = data['location']
            host = data['host']
            # print(competition_category, start_date, location)
            # print(Competition.objects.filter())
            competition = Competition.objects.get_or_create(competition_category=competition_category,
                                                            host=host,
                                                            location=location,
                                                            start_date=start_date,)
            print('competition: \n', competition, '\n')
            return JsonResponse({'competition_id': competition[0].pk})
        return render(request, 'resultregistration/resultregistration.html', context={'competition_id': 0})


class GroupFormView(AjaxFormMixin, FormView):
    form_class = GroupForm
    template_name = 'resultregistration/group_form.html'
    success_url = '/form-success/'

    def post(self, request, *args, **kwargs):
        # group_post = request.POST
        # print(group_post)
        group_form = GroupFormV2(request.POST)
        group_form.is_valid()
        competition_id = request.POST.get('competition_id')
        print(group_form.is_valid(), group_form.cleaned_data)
        group_fields = group_form.cleaned_data
        # data[competition'']=Competition.objects.get(pk=competition_id)
        # group_post['competition'] = competition_id
        # print(request.POST)
        # groupForm.competition = Competition.objects.get(pk=competition_id)
        print('\n {} \n'.format(competition_id))
        # print(groupForm)
        # print('group in post', groupForm.is_valid(), groupForm.cleaned_data, '\n', groupForm.errors)
        competition = Competition.objects.get(pk=competition_id)
        if group_form.is_valid() and competition:
            # TODONE: CHECK THAT GROUP IS NOT IN DB, AND CREATE
            # print(Group.objects.filter(competition=competition_id))
            print(competition)
            print('group valid')
            # competition.group_set.create(data)
            # group_fields = groupForm.__getattribute__('group_number')
            # print(groupForm.group_number)
            # group_fields = group_form.cleaned_data
            # print(group_fields)
            # group_fields
            group_query = competition.group_set.filter(group_number=int(group_fields['group_number']))
            if not group_query:
                group = Group.objects.create(
                    competition=competition,
                    group_number=group_fields['group_number'],
                    date=group_fields['date'],
                    status=group_fields['status'],
                    competition_leader=group_fields['competition_leader'],

                    secretary=group_fields['secretary'],
                    speaker=group_fields['speaker'],

                    technical_controller=group_fields['technical_controller'],
                    cheif_marshall=group_fields['cheif_marshall'],
                    time_keeper=group_fields['time_keeper'],

                    notes=group_fields['notes'],
                    records_description=group_fields['records_description'],
                    author=group_fields['author'],
                )
                # competitors are added by registering the results
                group.judges = group_fields['judges']
                group.jury = group_fields['jury']
                group.save()
                return JsonResponse({'group_id': group.pk})
                # jury = group_fields['jury'],
                # judges = group_fields['judges'],
                # competitiors = group_fields['competitors'],

                # print(clean_group['status'])
            # if not
            # print(group.cleaned_data)
            # data = groupForm.cleaned_data
            # group_number = data['group_number']
            # competition = data['competition']
            # group= Group.objects.get_or_create(competition=competition, )
            # if not Group.objects.filter(competition=competition_id, )

        return render(request, 'resultregistration/resultregistration.html', context={'group_id': -1})


class PendingResultFormView(AjaxFormMixin, FormView):
    form_class = PendingResultForm
    template_name = 'resultregistration/result_form.html'
    success_url = '/form-success'

    def post(self, request, *args, **kwargs):
        result = PendingResultForm(request.POST)
        group_id = request.POST['group_id']
        # print('enters post\n')
        # print(request.POST, '\n')
        group = Group.objects.get(pk=group_id)
        if result.is_valid() and group:
            # print('result valid')
            # print(result.cleaned_data)
            data = result.cleaned_data
            # TODO: MAKE THE FORM AUTOFIL TO PROPERLY GET THESE VALUES
            lifter_first = data['lifter_first_name']
            lifter_last = data['lifter_last_name']
            result_query = group.result_set.filter(lifter__first_name=lifter_first,
                                                   lifter__last_name=lifter_last)
            # print(lifter_first, lifter_last)
            lifter_query = Lifter.objects.filter(first_name=lifter_first, last_name=lifter_last)
            # print('lifter_query:\n', lifter_query, '\n')
            # lifter = Lifter.objects.get(lifter_query)
            lifter = lifter_query.first()

            # print('lifter: ', lifter)
            # print(result_query)

            if not result_query:
                age_group = data['category']

                result_instance = group.result_set.create(lifter=lifter,
                                                          body_weight=data['body_weight'],
                                                          age_group=age_group,
                                                          weight_class=data['weight_class'],
                                                          # age=14,
                                                          )
            else:
                result_instance = result_query.first()
            # add move_attempts
            # print('result_instance: ', result_instance)
            for i in range(1, 4):
                snatch = data['snatch{}'.format(i)]
                if str(snatch)[0].lower == 'n':
                    success = False
                    snatch = snatch[1:]
                else:
                    success = True
                # attempt_weight = snatch
                move_attempt = MoveAttempt.objects.filter(parent_result=result_instance,
                                                          move_type='Snatch',
                                                          attempt_num=i).first()
                if not move_attempt:
                    # print('\n move_attempt:\n{}\n'.format(move_attempt))
                    result_instance.moveattempt_set.create(move_type='Snatch',
                                                           attempt_num=i,
                                                           weight=snatch,
                                                           success=success)
                else:
                    move_attempt.weight = snatch
                    move_attempt.success = success
                    move_attempt.save()

            for i in range(1, 4):
                clean_and_jerk = data['clean_and_jerk{}'.format(i)]
                if str(clean_and_jerk)[0].lower() == 'n':
                    success = False
                    clean_and_jerk = clean_and_jerk[1:]
                else:
                    success = True
                # attempt_weight = clean_and_jerk
                # print('Parent_result = {}, move_type = {}, attempt_num = {}'.format(result_instance,
                #                                                                     'Clean and jerk',
                #                                                                     i))
                move_attempt = MoveAttempt.objects.filter(parent_result=result_instance.pk,
                                                          move_type='Clean and jerk',
                                                          attempt_num=i).first()
                # print(move_attempt)
                if not move_attempt:
                    # print('\n move_attempt:\n{}\n'.format(move_attempt))
                    result_instance.moveattempt_set.create(move_type='Clean and jerk',
                                                           attempt_num=i,
                                                           weight=clean_and_jerk,
                                                           success=success)
                else:
                    move_attempt.weight = clean_and_jerk
                    move_attempt.success = success
                    move_attempt.save()
            # print('success')
            # best_clean_and_jerk = get_best_clean_and_jerk_for_result()
            # pk = result_instance.pk,
            # result_data = {
            #     'age': get_age_for_lifter_in_result(pk),
            #     'best_clean_and_jerk': get_best_clean_and_jerk_for_result(pk),
            #     'best_snatch': get_best_snatch_for_result(pk),
            #     'points_with_sinclair': get_points_with_sinclair_for_result(pk),
            #     'points_with_veteran': get_points_with_veteran_for_result(pk)
            # }

            # returning dummy data before the methods are properly implemented and tested
            result_data = {
                'successful': True,
                'best_snatch': 10,
                'best_clean_and_jerk': 10,
                'total': 20,
                'point_with_sinclair': 25,
                'points_with_veteran': 0,
                'sinclair_coefficient': 1.25
            }
            # # result_data['success'] = True
            # result_data['age'] = 10
            # result_data[
            # result_data[
            # result_data['total'] = 20
            # result_data['points_with_sinclair'] = 25
            # result_data['points_with_veteran'] = 0
            # result_data['sinclair_coefficient'] = 1.25
        else:
            print(result.errors, '\n', result.cleaned_data)
            print('error')
            result_data = {'successful': False}
        return render(request, 'resultregistration/resultregistration.html', context=result_data)
    # def add_competition_if_not_exists(self):
    #
    #     if self.request.method == 'POST':
    #         competition = self.request.POST['competition_form']
    #         competition_category = competition.competition_category,
    #         start_date = competition.start_date,
    #         location = competition.location
    #         print(Competition.objects.filter(competition_category=competition_category,
    #                                           start_date=start_date,
    #                                           location=location))
    #         if not Competition.objects.filter(competition_category=competition_category,
    #                                           start_date=start_date,
    #                                           location=location):
    #             Competition.objects.create(competition_category=competition_category,
    #                                        start_date=start_date,
    #                                        location=location)
    #             print('yey object created')
    #         else:
    #             print('neyy, object exists')
    #         return self.request

    # def add_competition(FormView):
    #     context_instance = RequestContext(request)
    #     if request.method=='POST':
    #         competition = request.POST['competition_form']
    #         print('kommet inn i views')
    #         Competition.objects.Create(
    #             competition_category=competition.competition_category,
    #             start_date=competition.start_date,
    #             location=competition.location
    #         )
    #         print('ferdig med competitioncreate')
    #         return HttpResponse('')


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


def edit_result_clubofc(request, pk):
    group = Group.objects.filter(pk=pk)
    results = Result.objects.filter(group=group)
    context = {
        'pending_results': results,
        'groups': group
    }

    return render(request, 'resultregistration/editresult_clubofc.html', context)


def approve_group(request, pk):
    if not request.user.is_club_admin and not request.user.is_staff:  # hvis man ikke request ikke har rettigheter
        return HttpResponseRedirect('/home')
    group = Group.objects.get(pk=pk)
    group.status = "Godkjent"
    group.save()
    return redirect('/home/')


def reject_group(request, pk):
    if not request.user.is_club_admin and not request.user.is_staff:  # hvis man ikke request ikke har rettigheter
        return HttpResponseRedirect('/home')
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
