from django.contrib import admin

from users.models import User, Chat

admin.site.register(User)
admin.site.register(Chat)