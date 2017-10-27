from django.shortcuts import render, HttpResponse, Http404
import json
from .search.search import SearchFiltering
import athlitikos.settings as settings
from resultregistration.enums import AgeGroup, Gender, CompetitionCategory
from easy_pdf.rendering import render_to_pdf_response
from djqscsv import render_to_csv_response
from resultregistration.models import Competition


def generate_csv_report(request):
    """
    Generates a CSV file version of a search result.
    :param request:
    :return:
    """
    results = SearchFiltering.search_for_results_with_request(request).values('lifter__first_name',
                                                                              'lifter__last_name',
                                                                              'body_weight', 'age',
                                                                              'lifter__club__club_name',
                                                                              'age_group',
                                                                              'weight_class',
                                                                              'best_snatch',
                                                                              'best_clean_and_jerk',
                                                                              'total_lift',
                                                                              'sinclair_coefficient',
                                                                              'points_with_sinclair',
                                                                              'veteran_coefficient',
                                                                              'points_with_veteran')
    return render_to_csv_response(results)


def generate_report(request):
    """
    Generates a simple PDF version of a search result.
    :param request:
    :return:
    """
    if request.method == 'GET':
        results = SearchFiltering.search_for_results_with_request(request)
        return render_to_pdf_response(request=request,
                                      template='public/result-report-table.html',
                                      context={'results': results},
                                      download_filename='resultater.pdf',
                                      encoding='utf-8',
                                      )


def search(request):
    """
    The search page.
    Can generate a PDF of the result if is_pdf=true in the request.
    :param request:
    :return:
    """

    if request.method == 'GET' and request.is_ajax():
        results = SearchFiltering.search_for_results_with_request(request)
        return render(request, 'public/result-table.html', {'results': results})
    else:
        age_groups = map(lambda x: x[0], AgeGroup.choices())
        genders = map(lambda x: x[0], Gender.choices())
        return render(request, 'public/search.html', {'age_groups': age_groups, 'genders': genders})


def search_for_competitions(request):

    if request.is_ajax():

        category = request.GET.get('category')

        if category == "all":


        latest_competitions = Competition.objects.all()
        return render(request, 'public/competitions-table.html', {'latest_competitions': latest_competitions})
    else:
        categories = CompetitionCategory.choices()#map(lambda x: x[0], CompetitionCategory.choices())
        return render(request, 'public/competitions.html', {'categories': categories})


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


def get_age_groups(request):
    if request.is_ajax():
        gender = request.GET.get('selected_gender')
        all_groups = list(map(lambda x: x[0], AgeGroup.choices()))

        if gender is not None:
            groups = list(filter(lambda x: gender in x, all_groups))
        else:
            groups = all_groups

        data = json.dumps(groups)
    else:
        raise Http404()

    if settings.DEBUG:
        print(data)

    mime_type = 'application/json'
    return HttpResponse(data, mime_type)


def get_available_weight_classes(request):
    if request.is_ajax():
        age_group = request.GET.get('selected_age_group')
        weight_classes = AgeGroup.get_weight_classes(age_group)
        data = json.dumps(weight_classes)

    else:
        raise Http404()

    if settings.DEBUG:
        print(data)

    mime_type = 'application/json'
    return HttpResponse(data, mime_type)
