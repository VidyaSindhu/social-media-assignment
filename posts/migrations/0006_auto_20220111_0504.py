# Generated by Django 3.2.5 on 2022-01-11 05:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_rename_user_post_created_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commentonpost',
            old_name='user',
            new_name='commented_by',
        ),
        migrations.RenameField(
            model_name='postlikedby',
            old_name='user',
            new_name='liked_by',
        ),
    ]
