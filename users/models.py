from django.db import models
from django.contrib.auth.models import AbstractUser

# from chats.models import Chat


class User(AbstractUser):

    def dict_list():
        return {"0": []}
    
    def zapyty_dict():
        return {'wyslane': [], 'do_przyjecia': []}
    
    imie = models.CharField(null=True, max_length=20, verbose_name='Imię')
    nazwisko = models.CharField(null=True, max_length=30, verbose_name='Nazwisko')
    awatar = models.ImageField(null=True, blank=True, upload_to='media/user_avatars', default='default/default_avatar.png', verbose_name='Avatar')
    klasa = models.IntegerField(null=True, verbose_name='Klasa')
    kierunek = models.CharField(null=True, max_length=2, verbose_name='Kierunek')
    grupa = models.IntegerField(null=True, verbose_name='Grupa')

    czaty = models.JSONField(default=dict_list, verbose_name='Czaty') # List of Chat id's
    ostatni_czat = models.IntegerField(null=True, verbose_name="Ostatni czat") # Id of last opened chat
    zapyty_o_przyjacielstwie = models.JSONField(null=True, blank=True, default=zapyty_dict, verbose_name='Zapyty o dodaniu w przyjaciele')
    przyjaciele = models.JSONField(default=dict_list, verbose_name='Przyjaciele') # List of User id's


    class Meta:
        db_table = 'users.User'
        verbose_name = 'Użytkownik'
        verbose_name_plural = 'Użytkownicy'

    def __str__(self):
        return f'{self.imie} {self.nazwisko} {self.klasa}{self.kierunek}'
    
    def pelne_imie(self):
        return f'{self.imie} {self.nazwisko}'
    


class Chat(models.Model):
    def dict_list():
        return {"0": []}
    nazwa = models.CharField(null=True, blank=True, max_length=50, verbose_name='Nazwa')
    uczestnicy = models.JSONField(default=dict_list, verbose_name='Uczęstnicy')
    ikona = models.ImageField(null=True, blank=True, upload_to='media/chat_icons', default='default/default_chat.png', verbose_name='Ikonka')
    wiadomosci = models.JSONField(default=dict_list, verbose_name='Wiadomości') # List of messages
    # Przykład wiadomości:
    # {
    #     'nadawca': {
    #         'imie': '<pełne inmie>',
    #         'awatar': '...'
    #     },
    #     'tekst': '...',
    #     'czas_wysyłki': 'HH:MM | d.m.y'
    # }

    class Meta:
        db_table = 'users.Chat'
        verbose_name = 'Czat'
        verbose_name_plural = 'Czaty'


