# Generated by Django 5.1.6 on 2025-03-26 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_userdetails_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=10),
        ),
    ]
