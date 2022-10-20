# Generated by Django 4.1.2 on 2022-10-20 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_loginsessioninfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginsessioninfo',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loginsessioninfo',
            name='slug',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
    ]
