from django.contrib import admin
from .models import Workout

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'goal', 'training_level', 'is_ai_generated')
    list_filter = ('goal', 'training_level', 'is_ai_generated')
    search_fields = ('title', 'description')

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'video_url', 'video_file')
        }),
        ('Параметры тренировки', {
            'fields': ('goal', 'training_level', 'min_weight', 'max_weight')
        }),
        ('Повторение и расписание', {
            'fields': ('repeat_interval_weeks', 'repeat_days')
        }),
        ('Дополнительные параметры', {
            'fields': ('is_ai_generated',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """Делаем AI-тренировки доступными для редактирования"""
        if obj and obj.is_ai_generated:
            return []  # Если видео добавлено ИИ, оно редактируемое
        return ['is_ai_generated']