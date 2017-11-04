

def serialize_result(result):
    return {
        "lifter": result.lifter,
        "lifter_id": result.lifter_id,
        "club": result.lifter.club.club_name,
        "club_id": result.lifter.club.id,
        "birth_date": result.lifter.birth_date,
        "age_group": result.age_group,
        "weight_class": result.weight_class,
        "body_weight": result.body_weight,
    }


def serialize_group(group):
    pass

    group_data = {
        "group_number": group.group_number,
        "competition": group.competition,
        "date": group.date
    }

    results = []

    for result in group.result_set.all():
        results.append(serialize_result(result))

    return group_data, results
