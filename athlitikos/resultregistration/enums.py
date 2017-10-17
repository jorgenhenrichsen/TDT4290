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
    youth = 'U'
    junior = 'J'
    senior = 'S'
    master = 'M'


class Status(ChoiceEnum):
    approved = 'Godkjent'
    pending = 'Til godkjenning'
    denied = 'Ikke godkjent'
