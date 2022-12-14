# Generated by Django 4.1.2 on 2022-10-26 07:45

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_userprofile_user_followers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='background_pic',
            field=django_resized.forms.ResizedImageField(crop=None, default='default_cover.gif', force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[1200, 300], upload_to='background_pic'),
        ),
    ]
