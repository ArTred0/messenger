from django.shortcuts import render
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from users.forms import UserRegistrationForm, UserLoginForm
from users.models import User
from chats.models import Chat
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
        'title': 'Rejestracja',
        'form': form,
    }

    return render(request, 'users/registration.html', context=context)


def login(request):
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
            print('form invalid')
    else:
        form = UserLoginForm()

    context = {
        'title': 'Logowanie',
        'form': form
    }

    return render(request, 'users/login.html', context=context)


@login_required
def home(request):
    if request.method == 'POST':
        if request.POST['message_text']:
            chat = Chat.objects.get(nazwa=request.user.ostatni_czat)
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
    user_chats = [Chat.objects.get(nazwa=nazwa) for nazwa in request.user.czaty['0']]
    chat = Chat.objects.get(nazwa=request.user.ostatni_czat)
    messages_ = chat.wiadomosci['0']

    context = {
        'title': 'ZSMessenger - Główna',
        'user': request.user,
        'chats': user_chats,
        'messages_': messages_
    }
    print(request.user.przyjaciole)
    return render(request, 'users/home.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('users:login'))

@login_required
def add_chat(request):
    user: User = request.user
    user.czaty['0'].append(request.POST['group_name'])
    user.save()
    chat = Chat()
    chat.nazwa = request.POST['group_name']
    chat.save()
    return HttpResponseRedirect(reverse('users:home'))

@login_required
def chat(request, chat_name):
    user: User = request.user
    user.ostatni_czat = chat_name
    user.save()
    return HttpResponseRedirect(reverse('users:home'))


@login_required
def delete_message(request, id):
    chat = Chat.objects.get(nazwa=request.user.ostatni_czat)
    chat.wiadomosci['0'].reverse()
    for wiadomosc in chat.wiadomosci['0']:
        if wiadomosc['id'] == id:
            chat.wiadomosci['0'].reverse()
            chat.wiadomosci['0'].remove(wiadomosc)
            chat.save()
    return HttpResponseRedirect(reverse('users:home'))
