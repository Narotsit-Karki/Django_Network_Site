# Generated by Django 4.1.2 on 2022-10-19 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(default=' ', max_length=600, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='fname',
            field=models.CharField(default=' ', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='lname',
            field=models.CharField(default=' ', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='username',
            field=models.CharField(default=' ', max_length=800, unique=True),
            preserve_default=False,
        ),
    ]