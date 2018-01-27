from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from django.utils.translation import gettext


class InstructionsPG(Page):
    def is_displayed(self):
        return self.round_number == 1


class InstructionsCF(Page):
    def is_displayed(self):
        return self.round_number == 1


class PublicGood(Page):
    form_model = 'player'
    form_fields = ['contribution']

    def is_displayed(self):
        return self.round_number == 1


class CoopFace(Page):
    form_model = 'player'
    form_fields = ["choice_id"]

    def vars_for_template(self):
        self.player.coop_id = self.player.participant.vars["cooperators"][self.round_number-1]
        self.player.noncoop_id = self.player.participant.vars["defectors"][self.round_number-1]
        self.player.left_is_coop = self.player.participant.vars["left_is_coop"][self.round_number-1]
        return {
            "coop_pic": "coopfaceonline/{}.JPG".format(self.player.coop_id),
            "noncoop_pic": "coopfaceonline/{}.JPG".format(
                self.player.noncoop_id),
            "left_is_coop" : self.player.left_is_coop  # just to see it during the demo
        }


class Demographic(Page):
    form_model = "player"
    form_fields = ["age", "gender", "student", "student_level",
                   "student_discipline", "sport", "experience"]

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def error_message(self, values):
        if values["student"] and (values["student_level"] is None or
        values["student_discipline"] is None):
            return gettext("If you are a student you must select "
                           "your level of study and the displine "
                           "you are studying")


class End(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [InstructionsPG, PublicGood, InstructionsCF, CoopFace,
                 Demographic, End]
