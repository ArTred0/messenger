from django.urls import path
from users.views import register, login, logout, add_chat, chat, delete_message, home

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('add_chat/', add_chat, name='add_chat'),
    path('chat/<str:chat_name>', chat, name='chat'),
    path('delete_message/<int:id>', delete_message, name='delete_message'),
    path('', home, name='home'),
]
