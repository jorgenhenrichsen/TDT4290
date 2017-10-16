from django.shortcuts import render, HttpResponse, Http404
import json
from .search.search import SearchFiltering
import athlitikos.settings as settings
from resultregistration.enums import AgeGroup, Gender


def search(request):
    """
    The search page
    :param request:
    :return:
    """
    if request.method == 'GET' and request.is_ajax():

        lifters_json = request.GET.get('lifters')
        clubs_json = request.GET.get('clubs')
        lifters = None
        clubs = None

        if lifters_json is not None:
            lifters = json.loads(lifters_json)

        if clubs_json is not None:
            clubs = json.loads(clubs_json)

        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        results = SearchFiltering.search_for_results(lifters, clubs, from_date, to_date)

        return render(request, 'public/result-table.html', {'results': results})

    age_groups = map(lambda x: x[0], AgeGroup.choices())
    genders = map(lambda x: x[0], Gender.choices())

    return render(request, 'public/search.html', {'age_groups': age_groups, 'genders': genders})


def search_for_lifter(request):
    """
    Used for autompletion on lifter names
    :param request:
    :return:
    """
    if request.is_ajax():
        query = request.GET.get('term', '')

        lifters = SearchFiltering.search_for_lifter_containing(query)

        results = []
        for lifter in lifters:

            lifter_string = lifter.lifter.first_name +\
                            " " + lifter.lifter.last_name

            if lifter.club is not None:
                lifter_string += ", " + lifter.club.club_name

            lifter_json = {
                'label': lifter_string,
                'value': lifter_string,
                'id': lifter.lifter.id,
            }

            results.append(lifter_json)

        data = json.dumps(results)

    else:
        raise Http404()

    if settings.DEBUG:
        print(data)

    mime_type = 'application/json'
    return HttpResponse(data, mime_type)


def search_for_clubs(request):
    """
    Used for autompletion on club names
    :param request:
    :return:
    """
    if request.is_ajax():
        query = request.GET.get('term', '')
        clubs = SearchFiltering.search_for_club_containing(query)

        results = []
        for club in clubs:
            club_json = {
                'label': club.club_name,
                'value': club.club_name,
                'id': club.id,
            }
            results.append(club_json)

        data = json.dumps(results)

    else:
        raise Http404()

    if settings.DEBUG:
        print(data)

    mime_type = 'application/json'
    return HttpResponse(data, mime_type)


def get_available_weight_classes(request):
    if request.is_ajax():

        gender = request.GET.get('selected_gender')
        age_group = request.GET.get('selected_age_group')

        print(gender, age_group)

        weight_classes = [52, 67, 87, 110]  # TODO: Insert real classes
        data = json.dumps(weight_classes)

    else:
        raise Http404()

    if settings.DEBUG:
        print(data)

    mime_type = 'application/json'
    return HttpResponse(data, mime_type)
