# Generated by Django 3.2.5 on 2022-01-11 04:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_userfollower_delete_userfollowings'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['id']},
        ),
    ]
