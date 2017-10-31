from .models import Result, MoveAttempt, Sinclair, MelzerFaber
from datetime import date
from math import log10


def populate_sinclair(filepath='/static/coefficients/sinclairValues.txt'):
    infile = open(filepath)
    infile.readline()
    infile.readline()
    lines = infile.readlines()
    for i in range(len(lines)):
        sinclair_k_a = float(lines[i].split()[0])
        sinclair_k_b = float(lines[i].split()[1])
        sinclair_m_a = float(lines[i].split()[2])
        sinclair_m_b = float(lines[i].split()[3])
        year = float(lines[i].split()[4])
        Sinclair.objects.get_or_create(gender='M', sinclair_A=sinclair_m_a, sinclair_b=sinclair_m_b, year=year)
        Sinclair.objects.get_or_create(gender='K', sinclair_A=sinclair_k_a, sinclair_b=sinclair_k_b, year=year)


def populate_melzer_faber(filepath='/static/coefficients/meltzerFaberCoefficients.txt'):
    infile = open(filepath)
    year = int(infile.readline())
    for line in infile.readlines():
        coefs = line.split()
        print(coefs)
        try:
            for i in range(0, len(coefs), 2):
                print(coefs[i], coefs[i+1])
                MelzerFaber.objects.get_or_create(age=int(coefs[i]), coefficient=float(coefs[i+1]), year=year)
        except IndexError:
            continue


def set_result_sinclair_coefficient(pk, year=False):
    result = Result.objects.get(pk=pk)
    if not result:
        return False
    weight = result.body_weight
    gender = result.lifter.gender
    coefficient = 1
    if not year:
        sinclair_query = Sinclair.objects.filter(gender=gender)
        latest_year = 0
        sinclair = sinclair_query.first()
        for s in sinclair_query:
            if s.year > latest_year:
                latest_year = s.year
                sinclair = s
        if not sinclair:
            return False
        if weight < sinclair.sinclair_b:
            coefficient = 10**(sinclair.sinclair_A*(log10(weight/sinclair.sinclair_b)))
    else:
        sinclair = Sinclair.objects.get(gender=gender, year=year)
        if not sinclair:
            return False
        if weight < sinclair.sinclair_b:
            coefficient = 10**(sinclair.sinclair_A*(log10(weight/sinclair.sinclair_b)))
    result.sinclair_coefficient = coefficient
    result.save()
    return True


def get_best_snatch_for_result(pk):
    all_attempts = MoveAttempt.objects.filter(parent_result=pk, move_type='Snatch')
    best_attempt = 0
    for attempt in all_attempts:
        if attempt.success and attempt.weight > best_attempt:
            best_attempt = attempt.weight
    result = Result.objects.get(pk=pk)
    if not result:
        return {}
    result.best_snatch = best_attempt
    result.save()
    return {'best_snatch': str(best_attempt)}


def get_best_clean_and_jerk_for_result(pk):
    all_attempts = MoveAttempt.objects.filter(parent_result=pk, move_type='Clean and jerk')
    best_attempt = 0
    for attempt in all_attempts:
        if attempt.weight > best_attempt:
            best_attempt = attempt.weight
    result = Result.objects.get(pk=pk)
    if not result:
        return {}
    result.best_clean_and_jerk = best_attempt
    result.save()
    return {'best_clean_and_jerk': str(best_attempt)}


def get_lift_total_for_result(pk):
    result = Result.objects.get(pk=pk)
    if not result:
        return {}
    best_clean_and_jerk = result.best_clean_and_jerk
    best_snatch = result.best_snatch
    total_lift = best_snatch.weight+best_clean_and_jerk.weight
    result.total_lift = total_lift
    return {'total_lift': str(total_lift)}


def get_points_with_sinclair_for_result(pk):
    result = Result.objects.get(pk=pk)
    if not result:
        return {}
    total = result.total_lift*result.sinclair_coefficient
    result.points_with_sinclair = total
    result.save()
    return {'points_with_sinclair': str(total)}


def get_points_with_veteran_for_result(pk):
    result = Result.objects.get(pk=pk)
    if not result:
        return {}
    veteran_points = result.points_with_sinclair*result.veteran_coefficient
    result.points_with_veteran = veteran_points
    result.save()
    return {'points_with_veteran': str(veteran_points)}


def get_age_for_lifter_in_result(pk):
    result = Result.objects.get(pk=pk)
    if not result:
        return {}
    age = date.today().year - result.lifter.birth_date.year
    result.age = age
    result.save()
    return {'age': str(age)}
