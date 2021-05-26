from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, role=None, **extra_fields):

        if not email:
            raise ValueError('The Email must be set')

        email = self.normalize_email(email)
        if not role: role = self.model.GUEST

        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email, password, role, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email=email, password=password, role= role, **extra_fields)

class FitnessClubs(models.Model):
    CLUB_CHOICES = (
        (1, "Москва, ул. Вильгельма Пика, вл14, 4 этаж (МФК «Хуамин»)"),
        (2, "Москва, ул. Архитектора Власова, 22"),
        (3, "Москва, Каширское шоссе, 61Г"),
        (4, "Москва, ул. Климашкина, 17с2"),
        (5, "Санкт-Петербург, Пулковское ш., 35, ТРК Масштаб"),
        (6, "Санкт-Петербург, пл. Карла Фаберже, 8, литера Е"),
        (7, "Санкт-Петербург, ул. Коллонтай, 31, литера А, корп.1"),
        (8, "ул. Ю. Фучика, д. 90")
    )

    club_id = models.IntegerField(primary_key=True)
    address = models.TextField(unique=True, blank=True, null=True, choices=CLUB_CHOICES)
    city = models.TextField(blank=True, null=True)
    phone = models.TextField(unique=True, blank=True, null=True)

    class Meta:
        db_table = 'fitness_clubs'

class CustomUser(AbstractBaseUser, PermissionsMixin):

    CUSTOMER = 0
    INSTRUCTOR = 1
    ADMIN = 2
    SUPERUSER = 3
    GUEST = 4

    ROLE_CHOICES = (
        (CUSTOMER, 'Пользователь'),
        (INSTRUCTOR, 'Тренер'),
        (ADMIN, 'Администратор'),
        (SUPERUSER, 'Пользователь с абсолютными правами')
    )

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

    email = models.EmailField(verbose_name='email', unique=True)
    login = models.CharField(verbose_name='login', max_length=40, unique=True)
    role = models.PositiveSmallIntegerField(verbose_name='Роль',
        choices=ROLE_CHOICES, default=GUEST)
    club = models.PositiveSmallIntegerField(verbose_name='Фитнес клуб',
                                               choices=CLUB_CHOICES, default=1)
  #  phone = models.CharField(verbose_name='Телефон', max_length=40)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role', 'club', 'login']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

