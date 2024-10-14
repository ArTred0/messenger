from django.db import models
from django.contrib.auth.models import AbstractUser

# from chats.models import Chat


class User(AbstractUser):
    def d():
        return {"0": []}
    imie = models.CharField(null=True, max_length=20, verbose_name='Imię')
    nazwisko = models.CharField(null=True, max_length=30, verbose_name='Nazwisko')
    avatar = models.ImageField(null=True, blank=True, upload_to='media/user_avatars', default='default/default_avatar.png', verbose_name='Avatar')
    klasa = models.IntegerField(null=True, verbose_name='Klasa')
    kierunek = models.CharField(null=True, max_length=2, verbose_name='Kierunek')
    grupa = models.IntegerField(null=True, verbose_name='Grupa')

    czaty = models.JSONField(null=True, default=d, verbose_name='Czaty')
    ostatni_czat = models.CharField(null=True, max_length=50, default="", verbose_name="Ostatni czat")
    przyjaciole = models.JSONField(null=True, default=d, verbose_name='Przyjaciole')

    class Meta:
        db_table = 'users.User'
        verbose_name = 'Użytkownik'
        verbose_name_plural = 'Użytkownicy'

    def __str__(self):
        return f'{self.imie} {self.nazwisko} {self.klasa}{self.kierunek}'
    
    def pelne_imie(self):
        return f'{self.imie} {self.nazwisko}'

