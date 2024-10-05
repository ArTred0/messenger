from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

from users.models import User


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'imie',
            'nazwisko',
            'klasa',
            'kierunek',
            'grupa',
            'password1',
            'password2',
        ]
    imie = forms.CharField(max_length=20)
    nazwisko = forms.CharField(max_length=30)
    klasa = forms.IntegerField()
    kierunek = forms.CharField(max_length=2)
    grupa = forms.IntegerField()
    password1 = forms.CharField()
    password2 = forms.CharField()



class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = [
            'imie',
            'nazwisko',
            # 'username',
            'password',
        ]

    imie = forms.CharField(max_length=20)
    nazwisko = forms.CharField(max_length=30)
    # username = forms.CharField()
    password = forms.CharField()