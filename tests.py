from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random
from django.utils.translation import ugettext


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            yield (pages.Welcome)
            yield (pages.PGInstructions)
            yield (pages.PGDecision, {"PG_contribution": random.randint(0, Constants.endowment)})
            yield (pages.PGResults)
            yield (pages.CFInstructions)
        yield (pages.CFDecision, {"CF_choice": random.randint(0, 1)})
        if self.round_number == Constants.num_rounds:
            yield (pages.CFResults)
            yield (pages.Demographic,
                   {
                       "nationality": random.choice(
                           [
                               'Afghan', 'Albanian', 'Algerian', 'American',
                               'Andorran', 'Angolan',
                               'Antiguans', 'Argentinean', 'Armenian',
                               'Australian', 'Austrian',
                               'Azerbaijani', 'Bahamian', 'Bahraini',
                               'Bangladeshi', 'Barbadian',
                               'Barbudans', 'Batswana', 'Belarusian', 'Belgian',
                               'Belizean',
                               'Beninese', 'Bhutanese', 'Bolivian', 'Bosnian',
                               'Brazilian',
                               'British', 'Bruneian', 'Bulgarian', 'Burkinabe',
                               'Burmese',
                               'Burundian', 'Cambodian', 'Cameroonian',
                               'Canadian', 'Cape Verdean',
                               'Central African', 'Chadian', 'Chilean',
                               'Chinese', 'Colombian',
                               'Comoran', 'Congolese', 'Costa Rican',
                               'Croatian', 'Cuban',
                               'Cypriot', 'Czech', 'Danish', 'Djibouti',
                               'Dominican', 'Dutch',
                               'East Timorese', 'Ecuadorean', 'Egyptian',
                               'Emirian',
                               'Equatorial Guinean', 'Eritrean', 'Estonian',
                               'Ethiopian',
                               'Fijian', 'Filipino', 'Finnish', 'French',
                               'Gabonese', 'Gambian',
                               'Georgian', 'German', 'Ghanaian', 'Greek',
                               'Grenadian', 'Guatemalan',
                               'Guinea-Bissauan', 'Guinean', 'Guyanese',
                               'Haitian', 'Herzegovinian',
                               'Honduran', 'Hungarian', 'I-Kiribati',
                               'Icelander', 'Indian',
                               'Indonesian', 'Iranian', 'Iraqi', 'Irish',
                               'Israeli', 'Italian',
                               'Ivorian', 'Jamaican', 'Japanese', 'Jordanian',
                               'Kazakhstani',
                               'Kenyan', 'Kittian and Nevisian', 'Kuwaiti',
                               'Kyrgyz', 'Laotian',
                               'Latvian', 'Lebanese', 'Liberian', 'Libyan',
                               'Liechtensteiner',
                               'Lithuanian', 'Luxembourger', 'Macedonian',
                               'Malagasy', 'Malawian',
                               'Malaysian', 'Maldivian', 'Malian', 'Maltese',
                               'Marshallese',
                               'Mauritanian', 'Mauritian', 'Mexican',
                               'Micronesian', 'Moldovan',
                               'Monacan', 'Mongolian', 'Moroccan', 'Mosotho',
                               'Motswana',
                               'Mozambican', 'Namibian', 'Nauruan', 'Nepalese',
                               'New Zealander',
                               'Ni-Vanuatu', 'Nicaraguan', 'Nigerian',
                               'Nigerien', 'North Korean',
                               'Northern Irish', 'Norwegian', 'Omani',
                               'Pakistani', 'Palauan',
                               'Panamanian', 'Papua New Guinean', 'Paraguayan',
                               'Peruvian',
                               'Polish', 'Portuguese', 'Qatari', 'Romanian',
                               'Russian', 'Rwandan',
                               'Saint Lucian', 'Salvadoran', 'Samoan',
                               'San Marinese', 'Sao Tomean',
                               'Saudi', 'Scottish', 'Senegalese', 'Serbian',
                               'Seychellois',
                               'Sierra Leonean', 'Singaporean', 'Slovakian',
                               'Slovenian',
                               'Solomon Islander', 'Somali', 'South African',
                               'South Korean',
                               'Spanish', 'Sri Lankan', 'Sudanese', 'Surinamer',
                               'Swazi', 'Swedish',
                               'Swiss', 'Syrian', 'Taiwanese', 'Tajik',
                               'Tanzanian', 'Thai',
                               'Togolese', 'Tongan',
                               'Trinidadian or Tobagonian', 'Tunisian',
                               'Turkish', 'Tuvaluan', 'Ugandan', 'Ukrainian',
                               'Uruguayan',
                               'Uzbekistani', 'Venezuelan', 'Vietnamese',
                               'Welsh', 'Yemenite',
                               'Zambian', 'Zimbabwean']
                       ),
                       "age": random.randint(15, 90),
                       "gender": random.randint(0, 1),
                       "student": random.randint(0, 1),
                       "student_level": random.randint(0, 2),
                       "student_discipline": random.choice(
                           [ugettext("Economics"), ugettext("Law"),
                            ugettext("Medicine"),
                            ugettext("Computer science")]),
                       "student_scholarship": random.randint(0, 1),
                   })
            yield (pages.Final, {"comments": "Automatic message"})