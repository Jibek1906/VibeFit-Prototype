# Generated by Django 5.1.6 on 2025-03-27 10:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0008_dailynutrition_goal_calories_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dailynutrition',
            options={'ordering': ['-date'], 'verbose_name': 'Daily Nutrition', 'verbose_name_plural': 'Daily Nutrition'},
        ),
        migrations.AlterModelOptions(
            name='meal',
            options={'ordering': ['created_at']},
        ),
        migrations.AddField(
            model_name='dailynutrition',
            name='water_intake',
            field=models.PositiveIntegerField(default=0, help_text='In milliliters'),
        ),
        migrations.AddField(
            model_name='meal',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='meal',
            name='calories',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='meal',
            name='carbs',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='meal',
            name='fats',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='meal',
            name='proteins',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
