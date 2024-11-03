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
    o_sobie = models.TextField(default='Brak opisu', max_length=150, verbose_name='O sobie')
    klasa = models.IntegerField(null=True, verbose_name='Klasa')
    kierunek = models.CharField(null=True, max_length=2, verbose_name='Kierunek')
    grupa = models.IntegerField(null=True, verbose_name='Grupa')

    czaty = models.JSONField(default=dict_list, verbose_name='Czaty') # List of Chat id's
    ostatni_czat = models.IntegerField(null=True, verbose_name="Ostatni czat") # Id of last opened chat
    zapyty_o_przyjacielstwie = models.JSONField(null=True, blank=True, default=zapyty_dict, verbose_name='Zapyty o dodaniu w przyjaciele')
    przyjaciele = models.JSONField(default=dict_list, verbose_name='Przyjaciele') # List of User id's
    motyw = models.BooleanField(default=True, verbose_name='Motyw')


    class Meta:
        db_table = 'users.User'
        verbose_name = 'Użytkownik'
        verbose_name_plural = 'Użytkownicy'

    def __str__(self):
        return f'{self.imie} {self.nazwisko} {self.klasa}{self.kierunek}'
    
    def pelne_imie(self):
        return f'{self.imie} {self.nazwisko}'
    
    def dostepne_przyjaciele(self):
        return [self.__class__.objects.get(id=id) for id in self.przyjaciele['0']]
    


class Chat(models.Model):
    def dict_list():
        return {"0": []}
    adminy = models.JSONField(default=dict_list, verbose_name='Adminy')
    nazwa = models.CharField(null=True, blank=True, max_length=50, verbose_name='Nazwa')
    czy_grupa = models.BooleanField(default=True, verbose_name='Czy grupa')
    opis = models.TextField(default='Brak opisu', max_length=400, verbose_name='Opis')
    uczestnicy = models.JSONField(default=dict_list, verbose_name='Uczęstnicy') # List of User id's
    ikona = models.ImageField(null=True, blank=True, upload_to='chat_icons', default='default/default_chat.png', verbose_name='Ikonka')
    wiadomosci = models.JSONField(default=dict_list, verbose_name='Wiadomości') # List of messages
    # Przykład wiadomości:
    # {
    #     'nadawca': {
    #         'id': ...
    #         'imie': '<pełne imię>',
    #     },
    #     'tekst': '...',
    #     'czas_wysyłki': 'HH:MM | d.m.y'
    # }

    class Meta:
        db_table = 'users.Chat'
        verbose_name = 'Czat'
        verbose_name_plural = 'Czaty'


