from django.shortcuts import render
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from users.forms import UserRegistrationForm, UserLoginForm
from users.models import User, Chat
from users.utils import user_search, chat_search
import time
import json

def register(request: dict):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('users:home'))
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            # form.save()
            user:User = form.instance
            user.username = user.imie.lower()+'_'+user.nazwisko.lower()
            form.instance = user
            form.save()
            auth.login(request, user)
            return HttpResponseRedirect(reverse('users:home'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'ZSMessenger - Rejestracja',
        'form': form,
    }

    return render(request, 'users/registration.html', context=context)


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('users:home'))
    if request.method == 'POST':
        post = request.POST.copy()
        post.update({'username': request.POST['imie'].lower()+'_'+request.POST['nazwisko'].lower()})
        request.POST = post
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username=request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                if request.POST.get('next', None):
                    return HttpResponseRedirect(request.POST['next'])
                return HttpResponseRedirect(reverse('users:home'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'ZSMessenger - Logowanie',
        'form': form
    }

    return render(request, 'users/login.html', context=context)


@login_required
def home(request):
    if request.method == 'POST':
        if request.POST['message_text']:
            chat = Chat.objects.get(id=request.user.ostatni_czat)
            message = {
                'id': chat.wiadomosci['0'][-1]['id'] + 1 if chat.wiadomosci['0'] else 0,
                'nadawca': {
                    'id': request.user.id,
                    'imie': request.user.pelne_imie(),
                },
                'tekst': request.POST['message_text'],
                'czas_wysylki': time.strftime('%H:%M | %d.%m.%Y')
            }
            chat.wiadomosci['0'].append(message)
            chat.save()
            HttpResponseRedirect(reverse('users:home'))

    # user_chats = None

    user_chats = [Chat.objects.get(id=id) for id in request.user.czaty['0']] if request.user.czaty['0'] else None
    chat = Chat.objects.get(id=request.user.ostatni_czat) if request.user.ostatni_czat else None
    messages_ = chat.wiadomosci['0'] if chat else None


    context = {
        'title': 'ZSMessenger - Główna',
        'chats': user_chats,
        'messages_': messages_,
        'ostatni_nadawca': None,
    }
    
    return render(request, 'users/home.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('users:login'))


@login_required
def profile(request, username=None):
    if username:
        if username == request.user.username:
            return HttpResponseRedirect(reverse('users:profile'))
        user = User.objects.get(username=username)
        is_me = False
    else:
        
        user = request.user
        is_me = True

    chats = [Chat.objects.get(id=id) for id in user.czaty['0']]
    friends = [User.objects.get(id=id) for id in user.przyjaciele['0']]
    zapyty_dp = [User.objects.get(id=id) for id in user.zapyty_o_przyjacielstwie['do_przyjecia']]
    zapyty_w = [User.objects.get(id=id) for id in user.zapyty_o_przyjacielstwie['wyslane']]


    context = {
        'title': 'ZSMessenger - Profil',
        'user': user,
        'chats': chats,
        'friends': friends,
        'is_me': is_me,
        'zapyty_dp': zapyty_dp,
        'zapyty_w': zapyty_w,
    }
    return render(request, 'users/profile.html', context)


@login_required
def profile_info(request):
    if request.FILES:
        request.user.awatar = request.FILES['awatar']
    else:
        request.user.o_sobie = request.POST['o_sobie']
    
    request.user.save()
    
    return HttpResponseRedirect(reverse('users:profile'))


@login_required
def add_chat(request):
    chat = Chat()
    chat.nazwa = request.POST['nazwa']
    if request.FILES:
        chat.ikona = request.FILES['ikona']
    user_ids = list(request.POST.keys())
    user_ids.remove('csrfmiddlewaretoken')
    user_ids.remove('nazwa')
    if 'ikona' in user_ids:
        user_ids.remove('ikona')
    user_ids = list(map(int, user_ids)) if user_ids else []
    user_ids.append(request.user.id)
    user_ids.sort()
    chat.uczestnicy['0'] = user_ids
    chat.adminy['0'].append(request.user.id)
    chat.save()
    for id in user_ids:
        user = User.objects.get(id=id)
        user.czaty['0'].append(chat.id)
        user.save()
    request.user.czaty['0'].append(chat.id)
    request.user.save()
    return HttpResponseRedirect(reverse('users:home'))


@login_required
def chat(request, id):
    request.user.ostatni_czat = id
    request.user.save()
    return HttpResponseRedirect(reverse('users:home'))


@login_required
def chat_info(request, id):
    self = Chat.objects.get(id=id)
    if request.method == 'POST':
        if 'nazwa' in request.POST.keys():
            self.nazwa = request.POST['nazwa']
        if 'opis' in request.POST.keys():
            self.opis = request.POST['opis']
        elif request.FILES:
            self.ikona = request.FILES['ikona']
        self.save()

    uczestnicy = [User.objects.get(id=user) for user in self.uczestnicy['0']]
    adminy = [User.objects.get(id=user) for user in self.adminy['0']]

    przyjaciele = [User.objects.get(id=user) for user in request.user.przyjaciele['0'] if user not in self.uczestnicy['0']]
    

    context = {
        'title': 'ZSMessenger - Informacja o grupie',
        'self': self,
        'uczestnicy': uczestnicy,
        'przyjaciele': przyjaciele,
        'adminy': adminy
    }
    return render(request, 'users/chat_info.html', context)


@login_required
def add_member(request, group_id):
    keys = list(request.POST.keys())
    keys.remove('csrfmiddlewaretoken')
    new_members = list(map(int, keys))
    chat = Chat.objects.get(id=group_id)
    chat.uczestnicy['0'] += new_members
    chat.save()
    for id in new_members:
        user = User.objects.get(id=id)
        user.czaty['0'].append(group_id)
        user.save()
    
    return HttpResponseRedirect(reverse('users:chat_info', kwargs={'id': group_id}))


@login_required
def change_member_status(request, group_id, user_id):
    if request.user.id != user_id:
        chat = Chat.objects.get(id=group_id)
        if request.POST['status'] == 'admin':
            if user_id not in chat.adminy['0']:
                chat.adminy['0'].append(user_id)
                chat.save()
        else:
            if user_id in chat.adminy['0']:
                chat.adminy['0'].remove(user_id)
                chat.save()
    return HttpResponseRedirect(reverse('users:chat_info', kwargs={'id': group_id}))

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
def delete_message(request, id):
    chat = Chat.objects.get(id=request.user.ostatni_czat)
    chat.wiadomosci['0'].reverse()
    for wiadomosc in chat.wiadomosci['0']:
        if wiadomosc['id'] == id:
            chat.wiadomosci['0'].reverse()
            chat.wiadomosci['0'].remove(wiadomosc)
            chat.save()
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
def add_friend(request):
    if request.POST:
        usernames = list(request.POST.keys())
        usernames.remove('csrfmiddlewaretoken')
        for username in usernames:
            user = User.objects.get(username=username)
            if request.user.id in user.zapyty_o_przyjacielstwie['wyslane']:
                request.user.zapyty_o_przyjacielstwie['do_przyjecia'].remove(user.id)
                request.user.przyjaciele['0'].append(user.id)
                user.zapyty_o_przyjacielstwie['wyslane'].remove(request.user.id)
                user.przyjaciele['0'].append(request.user.id)
                user.save()
            elif user.id not in request.user.przyjaciele['0']:
                user.zapyty_o_przyjacielstwie['do_przyjecia'].append(request.user.id)
                user.save()
                request.user.zapyty_o_przyjacielstwie['wyslane'].append(user.id)
        request.user.save()


    # context = {
    #     'title': 'ZSMessenger - Profil'
    # }

    return HttpResponseRedirect(reverse('users:profile'))


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
def reject_friend(request, id):
    request.user.zapyty_o_przyjacielstwie['do_przyjecia'].remove(id)
    user_ = User.objects.get(id=id)
    user_.zapyty_o_przyjacielstwie['wyslane'].remove(request.user.id)
    request.user.save()
    user_.save()

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
def start_private(request, id):
    if chat:=Chat.objects.get(czy_grupa=False, uczestnicy={'0': [request.user.id, id]}):
        return HttpResponseRedirect(reverse('users:chat', kwargs={'id': chat.id}))
    elif chat:=Chat.objects.get(czy_grupa=False, uczestnicy={'0': [id, request.user.id]}):
        return HttpResponseRedirect(reverse('users:chat', kwargs={'id': chat.id}))
    chat = Chat(czy_grupa=False)
    chat.uczestnicy['0'] = [request.user.id, id]
    chat.save()
    request.user.czaty['0'].append(chat.id)
    request.user.save()
    
    return HttpResponseRedirect(reverse('users:chat', kwargs={'id': chat.id}))



def toggle_theme(request, state):
    request.user.motyw = True if state == 'light' else False
    request.user.save()
    return HttpResponse('success')
