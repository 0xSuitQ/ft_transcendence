# Generated by Django 5.1.2 on 2024-10-21 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_usertwofactorauthdata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='avatar_url',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
    ]
