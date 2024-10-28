# Generated by Django 5.1.2 on 2024-10-28 11:57

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_remove_tournament_winners_order'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchHistory2v2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player2', models.CharField(max_length=100)),
                ('player3', models.CharField(max_length=100)),
                ('player4', models.CharField(max_length=100)),
                ('winner1', models.CharField(blank=True, max_length=100, null=True)),
                ('winner2', models.CharField(blank=True, max_length=100, null=True)),
                ('match_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('match_score', models.CharField(max_length=50)),
                ('player1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_as_player1_2v2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]