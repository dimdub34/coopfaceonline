from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from django.utils.translation import ugettext, get_language


class Welcome(Page):
    def is_displayed(self):
        return self.round_number == 1


class Demographic(Page):
    form_model = "player"
    form_fields = ["nationality", "age", "gender", "student", "student_level",
                   "student_discipline", "student_scholarship"]

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def error_message(self, values):
        if values["student"] and values["student_scholarship"] is None:
            return ugettext("If you are a student you must tell if "
                           "you benefit from a scholarship.")


class Final(Page):
    form_model = "player"
    form_fields = ["comments"]

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


# ==============================================================================
#
# Public goods
#
# ==============================================================================

class PGInstructions(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            "convertion_rate": self.session.config[
                "real_world_currency_per_point"],
            "instructions_template": "coopfaceonline/PGInstructions_{}.html".format(get_language())}


class PGDecision(Page):
    form_model = 'player'
    form_fields = ['PG_contribution']

    def is_displayed(self):
        return self.round_number == 1


class PGResults(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {"indiv": Constants.endowment - self.player.PG_contribution}


# ==============================================================================
#
# Cooperation face
#
# ==============================================================================

class CFInstructions(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            "convertion_rate": self.session.config["real_world_currency_per_point"],
            "instructions_template": "coopfaceonline/CFInstructions_{}.html".format(get_language())}


class CFDecision(Page):
    form_model = 'player'
    form_fields = ["CF_choice"]

    def vars_for_template(self):
        self.player.CF_cooperator = \
            self.player.participant.vars["CF_cooperators"][self.round_number-1]
        self.player.CF_defector = \
            self.player.participant.vars["CF_defectors"][self.round_number-1]
        self.player.CF_cooperator_on_left = \
            self.player.participant.vars["CF_left_is_coop"][self.round_number-1]
        return {
            "coop_pic": "coopfaceonline/{}.JPG".format(self.player.CF_cooperator),
            "noncoop_pic": "coopfaceonline/{}.JPG".format(
                self.player.CF_defector),
            "left_is_coop" : self.player.CF_cooperator_on_left  # just to see it during the demo
        }

    def before_next_page(self):
        for p in self.group.get_players():
            p.set_cf_period_payoff()


class CFResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        selected_period = self.player.participant.vars["CF_period_selected_for_pay"]
        cf_choose_cooperator = self.player.in_round(selected_period).CF_choose_cooperator
        return {
            "CF_period_selected_for_pay": selected_period,
            "CF_choose_cooperator": cf_choose_cooperator
        }


page_sequence = [
    Welcome,
    PGInstructions, PGDecision, PGResults,
    CFInstructions, CFDecision, CFResults,
    Demographic, Final]
