import self as self
from django import forms
from .models import *
from users.models import FitnessClubs


from django import forms
import django_filters

from manager.repositories import FitnessClubsRepository
#
CLUB_CHOICES = (
    (1, "Москва, ул. Вильгельма Пика, вл14, 4 этаж (МФК «Хуамин»)"),
    (2, "Москва, ул. Архитектора Власова, 22"),
    (3, "Москва, Каширское шоссе, 61Г"),
    (4, "Москва, ул. Климашкина, 17с2"),
    (5, "Санкт-Петербург, Пулковское ш., 35, ТРК Масштаб"),
    (6, "Санкт-Петербург, пл. Карла Фаберже, 8, литера Е"),
    (7, "Санкт-Петербург, ул. Коллонтай, 31, литера А, корп.1"),
    (8, "Казань, ул. Ю. Фучика, д. 90")
)


class ClubForm(forms.Form):
    # club_c = []
    # clubs = FitnessClubs.objects.all()
    # for i in clubs:
    #     club_c.append((i.club_id, i.address))
    # address = forms.ChoiceField(choices= tuple(club_c))

    address = forms.ChoiceField(choices=CLUB_CHOICES, label="Адрес фитнес-клуба")

    # def __init__(self, user):
    #     self.user = user
    #     self.club_c = []
    #     self.clubs = FitnessClubsRepository.read_all(self.user)
    #     for i in self.clubs:
    #         self.club_c.append((i.club_id, i.address))
    #     address = forms.ChoiceField(choices= tuple(self.club_c))
    #     print(address)
