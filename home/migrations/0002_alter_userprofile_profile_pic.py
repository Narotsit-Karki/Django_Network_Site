# Generated by Django 4.1.2 on 2022-10-22 12:19

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=django_resized.forms.ResizedImageField(crop=None, default='default.png', force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[512, 512], upload_to='media/profile_pic'),
        ),
    ]
