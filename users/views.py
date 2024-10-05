from django.shortcuts import render
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from users.forms import UserRegistrationForm, UserLoginForm
from users.models import User

def register(request: dict):
    if request.user in User.objects.all():
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

    context = {
        'title': 'Home',
        'user': request.user,
    }
    return render(request, 'users/home.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('users:login'))


