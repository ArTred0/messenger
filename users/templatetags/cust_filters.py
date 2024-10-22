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
def imie(id):
    user = User.objects.get(id=id)
    return user.pelne_imie()


# @register.filter
# def user(id):
#     return User.objects.get(id=id)


@register.filter
def gt(value1, value2):
    return value1 > value2

@register.filter
def gte(value1, value2):
    return value1 >= value2

@register.filter
def lt(value1, value2):
    return value1 < value2

@register.filter
def lte(value1, value2):
    return value1 <= value2
