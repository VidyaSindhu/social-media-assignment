# Generated by Django 3.2.5 on 2022-01-11 04:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userfollower',
            options={'managed': True},
        ),
        migrations.AlterUniqueTogether(
            name='userfollower',
            unique_together={('user', 'follows')},
        ),
    ]
