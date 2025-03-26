# Generated by Django 5.1.4 on 2025-02-01 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0002_remove_workout_video_id_workout_day_of_week_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workout',
            name='duration',
        ),
        migrations.AddField(
            model_name='workout',
            name='max_weight',
            field=models.PositiveIntegerField(default=50),
        ),
        migrations.AddField(
            model_name='workout',
            name='min_weight',
            field=models.PositiveIntegerField(default=40),
        ),
        migrations.AlterField(
            model_name='workout',
            name='day_of_week',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=10),
        ),
        migrations.AlterField(
            model_name='workout',
            name='goal',
            field=models.CharField(choices=[('lose-weight', 'Lose Weight'), ('gain-muscle', 'Gain Muscle'), ('maintain', 'Maintain Weight')], max_length=50),
        ),
        migrations.AlterField(
            model_name='workout',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='workout',
            name='training_level',
            field=models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], max_length=50),
        ),
        migrations.AlterField(
            model_name='workout',
            name='video_url',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='workout',
            name='week_number',
            field=models.PositiveIntegerField(),
        ),
    ]
