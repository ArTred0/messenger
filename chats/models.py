from django.db import models
# from users.models import User


# class Message(models.Model):
#     nadawca = models.ForeignKey(to=User, on_delete=models.CASCADE)
#     tekst = models.TextField()
#     czas_wysylki = models.DateTimeField()

#     def jsonize(self):
#         return f'{{"nadawca": "{self.nadawca.username}", "tekst": "{self.tekst}", "czas_wysylki": "{self.czas_wysylki}"}}'


class Chat(models.Model):
    def d():
        return {"0": []}
    nazwa = models.CharField(max_length=50, verbose_name='Nazwa')
    icon = models.ImageField(upload_to='media/chat_icons', default='default/default_chat.png', verbose_name='Ikonka')
    wiadomosci = models.JSONField(default=d, verbose_name='Wiadomości')

    class Meta:
        db_table = 'chats.Chat'
        verbose_name = 'Czat'
        verbose_name_plural = 'Czaty'

