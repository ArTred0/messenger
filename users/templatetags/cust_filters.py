from django import template
import json
from time import strftime
from users.models import User

register = template.Library()

@register.filter
def eq(value, arg):
    return True if value == arg else False

@register.filter
def get_avatar(id):
    return User.objects.get(id=id).awatar.url

@register.filter
def get_last_message(chat):
    if chat.wiadomosci['0']:
        last_message = chat.wiadomosci['0'][-1]
    else:
        last_message = None
    
    return f"{last_message['nadawca']['imie']}: {last_message['tekst']}" if last_message else ""


@register.filter
def imie(id):
    user = User.objects.get(id=id)
    return user.pelne_imie()


@register.filter
def get_destination(seq, usr):
    seq.remove(usr)
    return User.objects.get(id=seq[0])



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
