# Generated by Django 3.2.5 on 2022-01-11 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20220111_0708'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['created_at']},
        ),
    ]