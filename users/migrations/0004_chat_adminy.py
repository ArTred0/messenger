# Generated by Django 4.2 on 2024-10-27 15:12

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_chat_opis_user_o_sobie_alter_chat_ikona'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='adminy',
            field=models.JSONField(default=users.models.Chat.dict_list, verbose_name='Adminy'),
        ),
    ]