# Generated by Django 5.1.6 on 2025-03-26 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_userdetails_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10),
        ),
    ]
