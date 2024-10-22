from django.shortcuts import render
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from users.forms import UserRegistrationForm, UserLoginForm
from users.models import User, Chat
from users.utils import q_search
import time

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
                    'imie': request.user.pelne_imie(),
                    'avatar': request.user.avatar.url
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
        'user': request.user,
        'chats': user_chats,
        'messages_': messages_
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
def add_chat(request):
    chat = Chat()
    chat.nazwa = request.POST['group_name']
    chat.save()
    user: User = request.user
    user.czaty['0'].append(request.POST['group_name'])
    user.save()
    return HttpResponseRedirect(reverse('users:home'))


@login_required
def chat(request, id):
    user: User = request.user
    user.ostatni_czat = id
    user.save()
    return HttpResponseRedirect(reverse('users:home'))


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
    users = q_search(username)
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
            if user.id not in request.user.przyjaciele['0']:
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
