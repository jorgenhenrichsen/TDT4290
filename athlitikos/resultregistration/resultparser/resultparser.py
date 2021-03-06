from resultregistration.models import Group, Lifter, Result, MoveAttempt
from resultregistration.enums import MoveTypes
import re


def is_success(attempt):
    """
    Defines if an attempt was successfull or not.
    Attempts are marked unsuccessfull by putting an "n" or a "-" in front of the weight attempted.
    :param attempt:
    :return:
    """
    if "n" in attempt or "N" in attempt or "-" in attempt:
        return False
    return True


def create_group_from_form(form, user):
    """
    Creates a group from the form.
    If a group with the group number and competition found in the form already exists, that will be updated with
    the new data, and returned.
    :param form: The GroupForm
    :param user: The user logged in, set as author
    :return: The Group if successfull, None if the form is invalid.
    """
    if bool(form) and form.is_valid():
        group_data = form.cleaned_data

        competition = group_data['competition']
        group_number = group_data['group_number']
        date = group_data['date']
        competition_leader = group_data.get('competition_leader')
        jury = group_data.get('jury')
        judges = group_data.get('judges')
        technical_controller = group_data.get('technical_controller')
        chief_marshall = group_data.get('chief_marshall')
        timekeeper = group_data.get('timekeeper')
        secretary = group_data.get('secretary')
        speaker = group_data.get('speaker')
        notes = group_data.get('notes')
        records_description = group_data.get('records_description')

        group = Group.objects.filter(competition_id__exact=competition.id, group_number__exact=group_number).first()

        if group is not None:
            print("Existing group, updating...")
            group.date = date
        else:
            print("Creating new group.")
            group = Group.objects.create(
                group_number=group_number,
                competition=competition,
                date=date,
                author=user,
            )

        group.competition_leader = competition_leader
        group.jury = jury
        group.judges = judges
        group.technical_controller = technical_controller
        group.chief_marshall = chief_marshall
        group.time_keeper = timekeeper
        group.secretary = secretary
        group.speaker = speaker
        group.notes = notes
        group.records_description = records_description
        group.save()

        return group

    return None


def create_move_attempt_from_form_data(form_data, parent_result, move_type, attempt_number):
    """
    Create a move attempt.
    If one exists with the same parent_result, move_type and attempt_number,
    that one will be updated with new data.
    :param form_data:
    :param parent_result:
    :param move_type:
    :param attempt_number:
    :return: The MoveAttempt, or None if unsuccessfull.
    """
    if bool(form_data):

        success = is_success(form_data)
        weight = int(re.sub("[^0-9]", "", form_data))

        attempt = MoveAttempt.objects.filter(parent_result__exact=parent_result,
                                             move_type__exact=move_type,
                                             attempt_num__exact=attempt_number).first()

        if attempt is None:
            attempt = MoveAttempt.objects.create(
                parent_result=parent_result,
                move_type=move_type,
                attempt_num=attempt_number,
                weight=weight,
                success=success,
            )
            return attempt
        else:
            attempt.success = success
            attempt.weight = weight
            attempt.save()
            return attempt

    return None


def create_result_from_form(result_form, group):
    """
    Create a Result, from form data.
    Will update if a result with the same group and lifter already exists.
    :param result_form:
    :param group:
    :return: The Result, is successfull.
    """

    if bool(result_form):

        lifter_id = result_form['lifter_id']
        lifter_name = result_form['lifter']
        club_name = result_form['club']

        if lifter_id is not None:
            lifter = Lifter.objects.get(pk=result_form['lifter_id'])
        elif lifter_name is not None and club_name is not None:
            names = lifter_name.rsplit(' ', 1)
            first_name = names[0]
            last_name = names[1]
            lifter = Lifter.objects.filter(first_name__icontains=first_name,
                                           last_name__icontains=last_name,
                                           club__club_name__icontains=club_name).first()
        else:
            return None

        body_weight = result_form['body_weight']
        age_group = result_form['age_group']
        weight_class = result_form['weight_class']

        result = Result.objects.filter(group__exact=group, lifter__exact=lifter).first()

        if result is None:
            result = Result.objects.create(
                group=group,
                lifter=lifter,
                body_weight=body_weight,
                age_group=age_group,
                weight_class=weight_class,
            )

        else:
            result.body_weight = body_weight
            result.age_group = age_group
            result.weight_class = weight_class

        snatches = [
            result_form['snatch_1'],
            result_form['snatch_2'],
            result_form['snatch_3'],
        ]

        c_and_js = [
            result_form['clean_and_jerk_1'],
            result_form['clean_and_jerk_2'],
            result_form['clean_and_jerk_3'],
        ]

        best_snatch = None
        best_clean_and_jerk = None

        for snatch in snatches:
            snatch_attempt = create_move_attempt_from_form_data(snatch,
                                                                result,
                                                                MoveTypes.snatch.value,
                                                                snatches.index(snatch))

            if snatch_attempt is not None and (best_snatch is None or best_snatch.weight < snatch_attempt.weight):
                    best_snatch = snatch_attempt

        for c_j in c_and_js:
            c_j_attempt = create_move_attempt_from_form_data(c_j,
                                                             result,
                                                             MoveTypes.clean_and_jerk.value,
                                                             c_and_js.index(c_j))

            if c_j_attempt is not None and\
                    (best_clean_and_jerk is None or best_clean_and_jerk.weight < c_j_attempt.weight):
                    best_clean_and_jerk = c_j_attempt

        result.best_snatch = best_snatch
        result.best_clean_and_jerk = best_clean_and_jerk

        if best_snatch is not None and best_clean_and_jerk is not None:
            result.total_lift = best_snatch.weight + best_clean_and_jerk.weight

            result.points_with_sinclair = result.total_lift * 1  # TODO: INSERT SINCLAIR COEFF HERE
            result.points_with_veteran = result.total_lift * 1  # TODO: INSER VETERAN COEFF HERE

        result.save()
        return result

    return None


def parse_result(group_form=None, result_formset=None, user=None):
    """
    Parses a result registration form, including a GroupForm and a ResultFormSet.
    :param group_form:
    :param result_formset:
    :param user:
    :return: The Group, the Results
    """
    if group_form.is_valid():

        group = create_group_from_form(form=group_form, user=user)

        if result_formset.is_valid():
            data = result_formset.cleaned_data
            print(data)
            results = []
            for result_form in data:
                result = create_result_from_form(result_form, group)
                if result is not None:
                    results.append(result)

            for result in results:
                group.competitors.add(result.lifter)

            group.save()
            return results, group
        else:
            print(result_formset.errors)
            return group

    else:
        print("Group form not valid, no results can be saved.")
        print(group_form.errors)

    return None
