from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random
from django.utils.translation import ugettext


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            yield (pages.PGInstructions)
            yield (pages.PGDecision, {"PG_contribution": random.randint(0, Constants.endowment)})
            yield (pages.CFInstructions)
        yield (pages.CFDecision, {"CF_choice": random.randint(0, 1)})
        if self.round_number == Constants.num_rounds:
            yield (pages.Demographic,
                   {
                       "age": random.randint(15, 90),
                       "gender": random.randint(0, 1),
                       "student": random.randint(0, 1),
                       "student_level": random.randint(0, 2),
                       "student_discipline": ugettext("Economics"),
                       "sport": random.randint(0, 1),
                       "experience": random.randint(0, 1)
                   })
            yield (pages.Final, {"comments": "Automatic message"})