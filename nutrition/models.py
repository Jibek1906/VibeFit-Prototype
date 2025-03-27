from django.db import models
from users.models import UserDetails

class DailyNutrition(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    date = models.DateField()
    calories = models.PositiveIntegerField(default=0)  # Добавлено
    proteins = models.PositiveIntegerField(default=0)  # Добавлено
    fats = models.PositiveIntegerField(default=0)      # Добавлено
    carbs = models.PositiveIntegerField(default=0)     # Добавлено

    class Meta:
        unique_together = ('user', 'date')
        verbose_name = 'Daily Nutrition'
        verbose_name_plural = 'Daily Nutrition'

    def __str__(self):
        return f"{self.user.user.username} - {self.date} - {self.calories} kcal"

class Meal(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snacks', 'Snacks'),
    ]
    
    nutrition = models.ForeignKey(DailyNutrition, on_delete=models.CASCADE, related_name='meals')
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    name = models.CharField(max_length=100)
    calories = models.PositiveIntegerField()
    proteins = models.PositiveIntegerField()
    fats = models.PositiveIntegerField()
    carbs = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.calories} kcal)"