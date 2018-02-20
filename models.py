from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django.utils.translation import ugettext
import random


author = 'Dimitri DUBOIS'

doc = """
Selection of cooperative players based on a picture of their face
"""


class Constants(BaseConstants):
    name_in_url = 'coopfaceonline'
    players_per_group = None

    # parameters
    endowment = 20
    mpcr = 0.6
    cooperators = ["1_201016", "11_120117", "11_160117", "17_090117", "5_120117", "7_090117", "7_171016"]
    defectors = ["1_081116", "1_130117", "1_181016", "11_090117", "13_090117", "15_211016", "5_171016"]
    num_rounds = len(cooperators)

    # codes
    defector = 0
    cooperator = 1

    # used in the treatment variable in the subsession class
    no_deaf = 0
    deaf_only = 1
    deaf_mix = 2

    # in_lab or online (used in subsession class)
    in_lab = 0
    online = 1


class Subsession(BaseSubsession):
    experimental_room = models.IntegerField()
    treatment = models.IntegerField()
    multiplier = models.FloatField()

    def creating_session(self):
        self.experimental_room = Constants.online
        self.treatment = self.session.config["treatment"]
        self.multiplier = Constants.mpcr * 2

        # creation of pairs of pictures
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars["CF_cooperators"] = Constants.cooperators.copy()
                random.shuffle(p.participant.vars["CF_cooperators"])
                p.participant.vars["CF_defectors"] = Constants.defectors.copy()
                random.shuffle(p.participant.vars["CF_defectors"])
                # we set the cooperator either on the left or on the right
                p.participant.vars["CF_left_is_coop"] = \
                    [random.randint(0, 1) for _ in range(Constants.num_rounds)]
                p.participant.vars["CF_period_selected_for_pay"] = random.randint(1, Constants.num_rounds)


class Group(BaseGroup):
    PG_group_contribution = models.IntegerField()


class Player(BasePlayer):

    deaf = models.IntegerField()

    # --------------------------------------------------------------------------
    # public goods
    # --------------------------------------------------------------------------

    PG_contribution = models.IntegerField(min=0, max=Constants.endowment)
    PG_payoff_individual_account = models.FloatField()
    PG_payoff_collective_account = models.FloatField()
    PG_payoff = models.CurrencyField()

    # --------------------------------------------------------------------------
    # Cooperation face
    # --------------------------------------------------------------------------

    CF_cooperator = models.StringField()
    CF_defector = models.StringField()
    CF_cooperator_on_left = models.BooleanField()
    CF_choice = models.IntegerField(
        choices=[(0, ugettext("Left")), (1, ugettext("Right"))],
        widget=widgets.RadioSelectHorizontal)
    CF_choose_cooperator = models.BooleanField()
    CF_number_of_cooperators_found = models.IntegerField()
    CF_period_selected_for_pay = models.BooleanField()
    CF_payoff = models.CurrencyField()
    CF_final_payoff = models.CurrencyField()

    # --------------------------------------------------------------------------
    # Demographic
    # --------------------------------------------------------------------------

    nationality = models.StringField(
        label=ugettext("What nationality are you?"),
        choices=[
            'Afghan', 'Albanian', 'Algerian', 'American', 'Andorran', 'Angolan',
            'Antiguans', 'Argentinean', 'Armenian', 'Australian', 'Austrian',
            'Azerbaijani', 'Bahamian', 'Bahraini', 'Bangladeshi', 'Barbadian',
            'Barbudans', 'Batswana', 'Belarusian', 'Belgian', 'Belizean',
            'Beninese', 'Bhutanese', 'Bolivian', 'Bosnian', 'Brazilian',
            'British', 'Bruneian', 'Bulgarian', 'Burkinabe', 'Burmese',
            'Burundian', 'Cambodian', 'Cameroonian', 'Canadian', 'Cape Verdean',
            'Central African', 'Chadian', 'Chilean', 'Chinese', 'Colombian',
            'Comoran', 'Congolese', 'Costa Rican', 'Croatian', 'Cuban',
            'Cypriot', 'Czech', 'Danish', 'Djibouti', 'Dominican', 'Dutch',
            'East Timorese', 'Ecuadorean', 'Egyptian', 'Emirian',
            'Equatorial Guinean', 'Eritrean', 'Estonian', 'Ethiopian',
            'Fijian', 'Filipino', 'Finnish', 'French', 'Gabonese', 'Gambian',
            'Georgian', 'German', 'Ghanaian', 'Greek', 'Grenadian', 'Guatemalan',
            'Guinea-Bissauan', 'Guinean', 'Guyanese', 'Haitian', 'Herzegovinian',
            'Honduran', 'Hungarian', 'I-Kiribati', 'Icelander', 'Indian',
            'Indonesian', 'Iranian', 'Iraqi', 'Irish', 'Israeli', 'Italian',
            'Ivorian', 'Jamaican', 'Japanese', 'Jordanian', 'Kazakhstani',
            'Kenyan', 'Kittian and Nevisian', 'Kuwaiti', 'Kyrgyz', 'Laotian',
            'Latvian', 'Lebanese', 'Liberian', 'Libyan', 'Liechtensteiner',
            'Lithuanian', 'Luxembourger', 'Macedonian', 'Malagasy', 'Malawian',
            'Malaysian', 'Maldivian', 'Malian', 'Maltese', 'Marshallese',
            'Mauritanian', 'Mauritian', 'Mexican', 'Micronesian', 'Moldovan',
            'Monacan', 'Mongolian', 'Moroccan', 'Mosotho', 'Motswana',
            'Mozambican', 'Namibian', 'Nauruan', 'Nepalese', 'New Zealander',
            'Ni-Vanuatu', 'Nicaraguan', 'Nigerian', 'Nigerien', 'North Korean',
            'Northern Irish', 'Norwegian', 'Omani', 'Pakistani', 'Palauan',
            'Panamanian', 'Papua New Guinean', 'Paraguayan', 'Peruvian',
            'Polish', 'Portuguese', 'Qatari', 'Romanian', 'Russian', 'Rwandan',
            'Saint Lucian', 'Salvadoran', 'Samoan', 'San Marinese', 'Sao Tomean',
            'Saudi', 'Scottish', 'Senegalese', 'Serbian', 'Seychellois',
            'Sierra Leonean', 'Singaporean', 'Slovakian', 'Slovenian',
            'Solomon Islander', 'Somali', 'South African', 'South Korean',
            'Spanish', 'Sri Lankan', 'Sudanese', 'Surinamer', 'Swazi', 'Swedish',
            'Swiss', 'Syrian', 'Taiwanese', 'Tajik', 'Tanzanian', 'Thai',
            'Togolese', 'Tongan', 'Trinidadian or Tobagonian', 'Tunisian',
            'Turkish', 'Tuvaluan', 'Ugandan', 'Ukrainian', 'Uruguayan',
            'Uzbekistani', 'Venezuelan', 'Vietnamese', 'Welsh', 'Yemenite',
            'Zambian', 'Zimbabwean'])
    age = models.IntegerField(
        label=ugettext('How old are you?'),
        min=13, max=125)
    gender = models.IntegerField(
        choices=[(0, ugettext('Female')), (1, ugettext('Male'))],
        label=ugettext('What is your gender?'),
        widget=widgets.RadioSelectHorizontal)
    student = models.IntegerField(
        choices=[(0, ugettext('No')), (1, ugettext('Yes'))],
        label=ugettext("Are you a student?"),
        widget=widgets.RadioSelectHorizontal)
    student_level = models.IntegerField(
        choices=[(0, ugettext('Bachelor')), (1, ugettext('Master')),
                 (2, ugettext('PhD')), (3, ugettext('Not in the list'))],
        label=ugettext("What is your level of study"))
    student_discipline = models.StringField(
        choices=[
            ugettext("Administration"), ugettext("Archeology"), ugettext("Biology"),
            ugettext("Buisiness school"), ugettext("Chemistry"),
            ugettext("Computer science"), ugettext("Economics"),
            ugettext("Education"), ugettext("Law"), ugettext("Management"),
            ugettext("Nursing school"), ugettext("Engineer"), ugettext("Geography"),
            ugettext("History"), ugettext("Lettres"), ugettext("Mathematics"),
            ugettext("Medicine"), ugettext("Music"), ugettext("Pharmacy"),
            ugettext("Philosophy"), ugettext("Physics"), ugettext("Politics"),
            ugettext("Sociology"), ugettext("Sport"), ugettext("Not in the list")
        ],
        label=ugettext("What are you studying ? / What did you study?"))
    student_scholarship = models.IntegerField(
        choices=[(0, ugettext('No')), (1, ugettext('Yes'))],
        label=ugettext("Do you benefit from a scholarship?"),
        widget=widgets.RadioSelectHorizontal, blank=True)
    student_scholarship_level = models.StringField(
        choices=[
            "0", "0 bis", "1", "2", "3", "4", "5", "6", "7"],
        label=ugettext("If you benefit a scholarship, what is its level?"),
        blank=True)
    comments = models.LongStringField(blank=True)

    def set_cf_period_payoff(self):
        """
        called at the end of each period
        :return:
        """
        # determine whether the subject found the cooperator
        if not self.CF_cooperator_on_left:
            self.CF_choose_cooperator = True if self.CF_choice == 1 else False
        else:
            self.CF_choose_cooperator = True if self.CF_choice == 0 else False

        # payoff depending on whether he found or not the cooperator
        self.CF_payoff = Constants.endowment * 2 * Constants.mpcr if \
            self.CF_choose_cooperator else Constants.endowment * \
                                           Constants.mpcr

        # set whether the current period is the period that will be paid
        if self.round_number == self.participant.vars["CF_period_selected_for_pay"]:
            self.CF_period_selected_for_pay = True
        else:
            self.CF_period_selected_for_pay = False

        # if last round
        if self.round_number == Constants.num_rounds:
            # compute the number of "good" answer
            self.CF_number_of_cooperators_found = sum(
                [p.CF_choose_cooperator for p in self.in_all_rounds()])
            # compute the part payoff
            self.CF_final_payoff = sum(
                [p.CF_payoff for p in self.in_all_rounds() if
                 p.CF_period_selected_for_pay])
            self.participant.vars["cf_payoff"] = self.CF_final_payoff
