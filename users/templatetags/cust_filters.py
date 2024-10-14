from django import template
import json
from time import strftime
from users.models import User

register = template.Library()

@register.filter
def eq(value, arg):
    return True if value == arg else False

@register.filter
def get_last_message(chat):
    if chat.wiadomosci['0']:
        last_message = chat.wiadomosci['0'][-1]
    else:
        last_message = None
    
    return f"{last_message['nadawca']['imie']}: {last_message['tekst']}" if last_message else ""

# @register.filter
# def czas(czas_int):
#     return strftime('%H:%M | %d.%m.%Y')

# @register.filter
# def avatar(username):
#     user = User.objects.get(username=username)
#     return user.avatar.url

@register.filter
def imie(username):
    # user = User.objects.get(username=username)
    return f"{username.split('_')[0].capitalize()} {username.split('_')[1].capitalize()}"
