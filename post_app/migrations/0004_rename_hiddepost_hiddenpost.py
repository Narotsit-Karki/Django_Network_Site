# Generated by Django 4.1.2 on 2022-10-23 11:10

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post_app', '0003_savedpost_hiddepost'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HiddePost',
            new_name='HiddenPost',
        ),
    ]
