from enum import Enum
import inspect


class ChoiceEnum(Enum):

    @classmethod
    def choices(cls):
        members = inspect.getmembers(cls, lambda m: not(inspect.isroutine(m)))
        properties = [m for m in members if not(m[0][:2] == '__')]
        choices = tuple([(str(p[1].value), p[0]) for p in properties])
        return choices


class JudgeLevel(ChoiceEnum):
    Level0 = 0
    Level1 = 1
    Level2 = 2
    Level3 = 3


class Gender(ChoiceEnum):
    male = 'M'
    female = 'K'


class MoveTypes(ChoiceEnum):
    snatch = 'Snatch'
    clean_and_jerk = 'Clean and jerk'


class AgeGroup(ChoiceEnum):

    youth_men = 'UM'
    youth_women = 'UK'
    junior_men = 'JM'
    junior_women = 'JK'
    senior_men = 'SM'
    senior_women = 'SK'

    master_men_35 = 'M1'
    master_men_40 = 'M2'
    master_men_45 = 'M3'
    master_men_50 = 'M4'
    master_men_55 = 'M5'
    master_men_60 = 'M6'
    master_men_65 = 'M7'
    master_men_70 = 'M8'
    master_men_75 = 'M9'

    master_women_35 = 'K1'
    master_women_40 = 'K2'
    master_women_45 = 'K3'
    master_women_50 = 'K4'
    master_women_55 = 'K5'
    master_women_60 = 'K6'
    master_women_65 = 'K7'
    master_women_70 = 'K8'
    master_women_75 = 'K9'

    @classmethod
    def get_weight_classes(cls, age_group):

        if age_group is None:
            return []

        standard_women = [
            "48",
            "53",
            "58",
            "63",
            "69",
            "75",
            "90",
            "+90",
        ]

        standard_men = [
            "56",
            "62",
            "69",
            "77",
            "85",
            "94",
            "105",
            "+105",
        ]

        youth_women = [
            "44",
            "48",
            "53",
            "58",
            "63",
            "69",
            "75",
            "+75",
        ]

        youth_men = [
            "50",
            "56",
            "62",
            "69",
            "77",
            "85",
            "94",
            "+94",
        ]

        if "M" in age_group:
            if "U" in age_group:
                return youth_men
            else:
                return standard_men
        else:
            if "U" in age_group:
                return youth_women
            else:
                return standard_women


class Status(ChoiceEnum):
    approved = 'Godkjent'
    pending = 'Til godkjenning'
    denied = 'Ikke godkjent'
