# Generated by Django 4.2 on 2024-10-13 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0003_alter_chat_wiadomosci'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='icon',
            field=models.ImageField(default='static/img/default_chat.png', upload_to='media/chat_icons', verbose_name='Ikonka'),
        ),
    ]