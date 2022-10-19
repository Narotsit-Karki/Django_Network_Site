# Generated by Django 4.1.2 on 2022-10-19 08:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=400)),
                ('address', models.CharField(max_length=500)),
                ('dob', models.DateField()),
                ('description', models.TextField(blank=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others'), ('', 'rather not say')], max_length=100)),
                ('job', models.TextField(blank=True)),
                ('profile_pic', models.ImageField(default='media/profile_pic/default.png', upload_to='media/profile_pic')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]