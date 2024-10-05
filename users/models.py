from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    imie = models.CharField(max_length=20, verbose_name='Imię')
    nazwisko = models.CharField(max_length=30, verbose_name='Nazwisko')
    avatar = models.ImageField(null=True, blank=True, upload_to='media/user_avatars', verbose_name='Avatar')
    klasa = models.IntegerField(verbose_name='Klasa')
    kierunek = models.CharField(max_length=2, verbose_name='Kierunek')
    grupa = models.IntegerField(verbose_name='Grupa')

    class Meta:
        db_table = 'users.User'
        verbose_name = 'Użytkownik'
        verbose_name_plural = 'Użytkownicy'

    def __str__(self):
        return f'{self.imie} {self.nazwisko} {self.klasa}{self.kierunek}'

