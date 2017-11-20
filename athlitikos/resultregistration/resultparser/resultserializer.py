from resultregistration.models import MoveAttempt
from resultregistration.enums import MoveTypes
from datetime import datetime

def serialize_result(result):

    birth_date = result.lifter.birth_date.strftime("%d/%m/%Y")

    data = {
        "lifter": result.lifter,
        "lifter_id": result.lifter_id,
        "club": result.lifter.club.club_name,
        "club_id": result.lifter.club.id,
        "birth_date": birth_date,
        "age_group": result.age_group,
        "weight_class": result.weight_class,
        "body_weight": result.body_weight,
    }

    attempts = MoveAttempt.objects.filter(parent_result__exact=result)
    snatches = attempts.filter(move_type__exact=MoveTypes.snatch.value).order_by('attempt_num')
    c_js = attempts.filter(move_type__exact=MoveTypes.clean_and_jerk.value).order_by('attempt_num')

    snatch_dict = {}
    for i in range(0, len(snatches)):
        snatch_dict["snatch_{}".format(i+1)] = snatches[i].weight
    data.update(snatch_dict)

    c_j_dict = {}
    for i in range(0, len(c_js)):
        c_j_dict["clean_and_jerk_{}".format(i+1)] = c_js[i].weight
    data.update(c_j_dict)

    return data


def serialize_group(group):

    date = group.date.strftime("%d/%m/%Y")

    group_data = {
        "group_number": group.group_number,
        "competition": group.competition,
        "date": date,
        "competition_leader": group.competition_leader,
        "jury": group.jury.all(),
        "judges": group.judges.all(),
        "technical_controller": group.technical_controller,
        "chief_marshall": group.chief_marshall,
        "timekeeper": group.time_keeper,
        "secretary": group.secretary,
        "speaker": group.speaker,
        "notes": group.notes,
        "records_description": group.records_description,
    }

    results = []

    for result in group.result_set.all():
        results.append(serialize_result(result))

    return group_data, results
