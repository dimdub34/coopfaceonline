from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django.utils.translation import gettext
import random


author = 'Dimitri DUBOIS'

doc = """
Public good and selection of cooperative partner based on a picture of 
their face
"""


class Constants(BaseConstants):
    name_in_url = 'coopfaceonline'
    players_per_group = None
    endowment = 20
    mpcr = 0.6
    noncoop = 0
    coop = 1
    cooperators = ["1_201016", "11_120117", "11_160117", "17_090117", "5_120117", "7_090117", "7_171016"]
    defectors = ["1_081116", "1_130117", "1_181016", "11_090117", "13_090117", "15_211016", "5_171016"]
    num_rounds = len(cooperators)
    no_deaf = 0
    deaf_only = 1
    deaf_mix = 2


class Subsession(BaseSubsession):

    def creating_session(self):
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars["cooperators"] = Constants.cooperators.copy()
                random.shuffle(p.participant.vars["cooperators"])
                p.participant.vars["defectors"] = Constants.defectors.copy()
                random.shuffle(p.participant.vars["defectors"])
                # on détermine si à gauche ou à droite on met la photo du
                # coopérateur / défecteur
                p.participant.vars["left_is_coop"] = \
                    [random.randint(0, 1) for _ in range(Constants.num_rounds)]
                p.participant.vars["period_selected_for_pay"] = random.randint(1, Constants.num_rounds)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    deaf = models.IntegerField()
    contribution = models.IntegerField(min=0, max=Constants.endowment)
    coop_id = models.StringField()
    noncoop_id = models.StringField()
    left_is_coop = models.BooleanField()
    choice_id = models.PositiveIntegerField(
        choices=[(0, gettext("left")), (1, gettext("right"))],
        widget=widgets.RadioSelectHorizontal)
    choose_cooperator = models.BooleanField()
    number_of_cooperators_found = models.IntegerField()
    age = models.IntegerField(
        verbose_name=gettext('What is your age?'),
        min=13, max=125)
    gender = models.IntegerField(
        choices=[(0, gettext('Female')), (1, gettext('Male'))],
        verbose_name=gettext('What is your gender?'),
        widget=widgets.RadioSelectHorizontal)
    student = models.IntegerField(
        choices=[(0, gettext('No')), (1, gettext('Yes'))],
        verbose_name=gettext("Are you a student?"),
        widget=widgets.RadioSelectHorizontal)
    student_level = models.IntegerField(
        choices=[(0, gettext('Bachelor')), (1, gettext('Master')),
                 (3, gettext('PhD')), (4, gettext('Not in the list'))],
        blank=True)
    student_discipline = models.StringField(
        choices=["Administration", "Archeology", "Biology", "Buisiness school",
                 "Chemistry", "Computer science", "Economics","Education",
                 "Law", "Management", "Nursing school", "Engineer",
                 "Geography", "History", "Lettres", "Mathematics", "Medicine",
                 "Music", "Pharmacy", "Philosophy", "Physics", "Politics",
                 "Sociology", "Sport", "Not in the list"],
        verbose_name=gettext("What are you studying?"), blank=True)
    sport = models.IntegerField(
        choices=[(0, gettext('No')), (1, gettext('Yes'))],
        verbose_name=gettext("Do you pratice (regularly) some sport?"),
        widget=widgets.RadioSelectHorizontal)
    experience = models.IntegerField(
        choices=[(0, gettext('No')), (1, gettext('Yes'))],
        verbose_name=gettext("Have you ever participated in an experiment?"),
        widget=widgets.RadioSelectHorizontal)

    def set_period_payoff(self):
        if not self.left_is_coop:  # defector on the left on the screen
            self.choose_cooperator = True if self.choice_id == 1 else False
        else:  # cooperator on the left side of pictures
            self.choose_cooperator = True if self.choice_id == 0 else False

