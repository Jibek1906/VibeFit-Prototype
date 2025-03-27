# Generated by Django 5.1.6 on 2025-03-26 19:50

import django.core.serializers.json
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_userdetails_weight'),
        ('workouts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userworkouthistory',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userworkouthistory',
            name='workout',
        ),
        migrations.RemoveField(
            model_name='workout',
            name='category',
        ),
        migrations.CreateModel(
            name='WorkoutHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workout_date', models.DateField()),
                ('workout_type', models.CharField(max_length=100)),
                ('duration', models.IntegerField()),
                ('difficulty', models.IntegerField(choices=[(1, 'Easy'), (2, 'Medium'), (3, 'Hard')])),
                ('notes', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userdetails')),
            ],
            options={
                'verbose_name_plural': 'Workout Histories',
            },
        ),
        migrations.CreateModel(
            name='WorkoutPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('plan_data', models.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userdetails')),
            ],
            options={
                'unique_together': {('user', 'start_date', 'end_date')},
            },
        ),
        migrations.DeleteModel(
            name='GeneratedWorkoutPlan',
        ),
        migrations.DeleteModel(
            name='UserWorkoutHistory',
        ),
        migrations.DeleteModel(
            name='Workout',
        ),
        migrations.DeleteModel(
            name='WorkoutCategory',
        ),
    ]
