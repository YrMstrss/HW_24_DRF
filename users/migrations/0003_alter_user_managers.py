# Generated by Django 4.2.6 on 2023-11-06 13:32

import django.contrib.auth.models
from django.db import migrations
import users.managers


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options_remove_user_username_user_avatar_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('object', users.managers.UserManager()),
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
