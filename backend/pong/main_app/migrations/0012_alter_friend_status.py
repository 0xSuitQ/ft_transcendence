# Generated by Django 5.1.2 on 2024-10-21 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_remove_userprofile_avatar_url_userprofile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
    ]
