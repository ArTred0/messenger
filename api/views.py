from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from api.utils import user_search, chat_search
from users.models import User, Chat

import time
import json

# Create your views here.


@login_required
def check_new_messages(request, id):
    chat = Chat.objects.get(id=request.user.ostatni_czat)
    if id:
        messages = chat.wiadomosci['0'][id:]
    else:
        messages = []

    return JsonResponse({'0': messages})


@login_required
def send_message(request):
    chat = Chat.objects.get(id=request.user.ostatni_czat)
    message = {
        'id': len(chat.wiadomosci['0']) if chat.wiadomosci['0'] else 0,
        'nadawca': {
            'id': request.user.id,
            'imie': request.user.pelne_imie(),
        },
        'tekst': json.loads(request.body)['tekst'],
        'czas_wysylki': time.strftime('%H:%M | %d.%m.%Y')
    }
    chat.wiadomosci['0'].append(message)
    chat.save()
    return JsonResponse(message)


@login_required
def delete_message(request, id):
    chat = Chat.objects.get(id=request.user.ostatni_czat)
    messages = list(enumerate(chat.wiadomosci['0']))
    messages.reverse()
    for ms_id, message in messages:
        if message['id'] == id:
            del chat.wiadomosci['0'][ms_id]
            break
    chat.save()
    return HttpResponse('success')


@login_required
def change_message(request):
    data = json.loads(request.body)
    message_id = int(data['ms_id'])
    chat = Chat.objects.get(id=request.user.ostatni_czat)
    chat.wiadomosci['0'][message_id]['tekst'] = data['new_text']
    chat.save()
    return HttpResponse('success')
    


@login_required
def search_chat(request, name):
    chats = chat_search(name)
    resp = {}
    resp['0'] = []
    for chat in chats:
        if not chat in request.user.czaty['0']:
            resp['0'].append({
                'id': chat.id,
                'img': chat.ikona.url,
                'name': chat.nazwa,
                'users': len(chat.uczestnicy['0'])
                })
            # resp.append(f'{user.pelne_imie()} {user.klasa}{user.kierunek}-{user.grupa}')
    return HttpResponse(json.dumps(resp)) if resp['0'] else HttpResponse('')



@login_required
def enter_chat(request, id):
    chat = Chat.objects.get(id=id)
    if not request.user.id in chat.uczestnicy['0']:
        chat.uczestnicy['0'].append(request.user.id)
        chat.save()
        request.user.czaty['0'].append(chat.id)
        request.user.ostatni_czat = chat.id
        request.user.save()
    else:
        return HttpResponseRedirect(reverse('users:chat', kwargs={'id': id}))

    return HttpResponse('success')


@login_required
def remove_member(request, group_id, user_id):
    if user_id != request.user.id:
        group = Chat.objects.get(id=group_id)
        user = User.objects.get(id=user_id)
        group.uczestnicy['0'].remove(user_id)
        user.czaty['0'].remove(group_id)
        group.save()
        user.save()

        return HttpResponse('success')
    

@login_required
def leave_group(request, id):
    chat = Chat.objects.get(id=id)
    chat.uczestnicy['0'].remove(request.user.id)
    if request.user.id in chat.adminy['0']:
        chat.adminy['0'].remove(request.user.id)
    request.user.czaty['0'].remove(id)
    if chat.uczestnicy['0']:
        chat.save()
    else:
        chat.delete()
    request.user.save()

    return HttpResponse('success')


@login_required
def delete_group(request, id):
    chat = Chat.objects.get(id=id)
    members = chat.uczestnicy['0']
    for usr_id in members:
        user = User.objects.get(id=usr_id)
        user.czaty['0'].remove(id)
        if user.ostatni_czat == id:
            user.ostatni_czat = None
        user.save()
    chat.delete()

    return HttpResponseRedirect(reverse('users:home'))


@login_required
def search_user(request, username):
    users = user_search(username)
    resp = []
    for user in users:
        if user != request.user and not (user.id in request.user.przyjaciele['0'] or user.id in request.user.zapyty_o_przyjacielstwie['wyslane'] or user.id in request.user.zapyty_o_przyjacielstwie['do_przyjecia']):
            resp.append(f'{user.pelne_imie()} {user.klasa}{user.kierunek}-{user.grupa}')
    # users.exclude(request.user)
    return HttpResponse(str(resp)[1:-1])


@login_required
def reject_friend(request, id):
    request.user.zapyty_o_przyjacielstwie['do_przyjecia'].remove(id)
    user_ = User.objects.get(id=id)
    user_.zapyty_o_przyjacielstwie['wyslane'].remove(request.user.id)
    request.user.save()
    user_.save()

    return HttpResponse('success')


@login_required
def accept_friend(request, id):
    request.user.zapyty_o_przyjacielstwie['do_przyjecia'].remove(id)
    friend = User.objects.get(id=id)
    friend.zapyty_o_przyjacielstwie['wyslane'].remove(request.user.id)
    request.user.przyjaciele['0'].append(friend.id)
    friend.przyjaciele['0'].append(request.user.id)
    request.user.save()
    friend.save()

    return HttpResponse('success')


@login_required
def delete_friend(request, id):
    request.user.przyjaciele['0'].remove(id)
    request.user.save()
    user = User.objects.get(id=id)
    user.przyjaciele['0'].remove(request.user.id)
    user.save()

    return HttpResponse('succes')


@login_required
def cancel_request(request, id):
    request.user.zapyty_o_przyjacielstwie['wyslane'].remove(id)
    user = User.objects.get(id=id)
    user.zapyty_o_przyjacielstwie['do_przyjecia'].remove(request.user.id)
    request.user.save()
    user.save()

    return HttpResponse('success')


def toggle_theme(request, state):
    request.user.motyw = True if state == 'light' else False
    request.user.save()
    return HttpResponse('success')