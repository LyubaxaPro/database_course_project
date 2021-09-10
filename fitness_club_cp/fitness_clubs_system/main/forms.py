import self as self
from django import forms
from manager.models import Customers, Instructors
from users.models import CustomUser
from django import forms
#
from .widgets import BootstrapDateTimePickerInput

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

    address = forms.ChoiceField(choices=CLUB_CHOICES, label="Адрес фитнес-клуба")

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ('name', 'surname', 'patronymic', 'day_of_birth', 'height', 'tariff', 'tariff_end_date')

class CustomerEditProfileForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ('name', 'surname', 'patronymic', 'day_of_birth', 'height')

class AddMeasureForm(forms.Form):

    weight = forms.IntegerField(label="Вес")
    date = forms.DateField(label="Дата")

class InstructorProfileForm(forms.ModelForm):
    class Meta:
        model = Instructors
        photo = forms.ImageField(widget=forms.FileInput())
        fields = ('name', 'surname', 'patronymic', 'education', 'experience', 'achievements', 'specialization', 'photo')


class InstructorEditProfileForm(forms.ModelForm):
    class Meta:
        model = Instructors
        photo = forms.ImageField(widget=forms.FileInput())
        fields = ('name', 'surname', 'patronymic', 'education', 'experience', 'achievements', 'specialization')