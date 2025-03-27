# Generated by Django 5.1.6 on 2025-03-27 12:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_remove_userprofile_avatar_userprofile_birth_date_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='gender',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='goal',
            field=models.CharField(choices=[('Lose Weight', 'Lose Weight'), ('Gain Muscle', 'Gain Muscle'), ('Maintain', 'Maintain Weight')], default='Maintain', max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='height',
            field=models.PositiveIntegerField(default=150),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='training_level',
            field=models.CharField(choices=[('Beginner', 'Beginner'), ('Int ermediate', 'Intermediate'), ('Advanced', 'Advanced')], default='Beginner', max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
