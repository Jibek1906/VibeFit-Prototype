from django.db import models
from users.models import UserDetails

class Workout(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    video_url = models.URLField(null=True, blank=True)
    video_file = models.FileField(upload_to='workouts/', null=True, blank=True)
    goal = models.CharField(max_length=50)
    training_level = models.CharField(max_length=50)
    min_weight = models.DecimalField(max_digits=5, decimal_places=2)
    max_weight = models.DecimalField(max_digits=5, decimal_places=2)
    repeat_interval_weeks = models.IntegerField()
    repeat_days = models.JSONField(default=list)
    week_number = models.IntegerField(null=True, blank=True)
    is_ai_generated = models.BooleanField(default=True)  # Флаг, отмечающий, что видео добавлено ИИ

    def __str__(self):
        return self.title