# Generated by Django 4.0.1 on 2022-01-10 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfollower',
            old_name='follow',
            new_name='follows',
        ),
    ]