# Generated by Django 4.0.1 on 2022-01-10 18:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_follow_userfollower_follows'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfollower',
            name='follows',
        ),
        migrations.AddField(
            model_name='userfollower',
            name='follows',
            field=models.ManyToManyField(related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='userfollower',
            name='user',
        ),
        migrations.AddField(
            model_name='userfollower',
            name='user',
            field=models.ManyToManyField(related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
