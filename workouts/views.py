import random
from datetime import timedelta, datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Workout
from users.models import UserDetails, WeightRecord
from .youtube_api import search_youtube_videos

@login_required
def workouts_api(request):
    """API для подбора тренировок с учетом уровня и цели пользователя."""
    try:
        user_details = UserDetails.objects.get(user=request.user)
    except UserDetails.DoesNotExist:
        return JsonResponse({"error": "User details not found"}, status=400)

    # Количество тренировок в день по уровню подготовки
    workout_count_map = {
        'beginner': 3,
        'intermediate': 4,
        'advanced': 5
    }
    num_workouts = workout_count_map.get(user_details.training_level, 3)

    # Подбираем тренировки
    query = f"{user_details.goal} {user_details.training_level} workout"
    workouts = search_youtube_videos(query, max_results=15)

    if not workouts:
        return JsonResponse({"error": "No workouts found"}, status=400)

    # Выбираем нужное количество тренировок на день
    selected_workouts = random.sample(workouts, min(len(workouts), num_workouts))

    # Генерация JSON-ответа
    workout_schedule = []
    for workout in selected_workouts:
        workout_schedule.append({
            "title": workout["title"],
            "video_url": workout["video_url"],
            "thumbnail": workout["thumbnail"],
            "embed_url": workout["embed_url"] if workout["embed_url"] else None,
            "watch_on_youtube": workout["video_url"] if not workout["embed_url"] else None
        })

    return JsonResponse({"workouts": workout_schedule}, safe=False)

@login_required
def workouts_view(request):
    """Рендеринг страницы тренировок"""
    try:
        user_details = UserDetails.objects.get(user=request.user)
        registration_date = request.user.date_joined.date()
    except UserDetails.DoesNotExist:
        registration_date = datetime.now().date()

    context = {
        'registration_date': registration_date.strftime("%Y-%m-%d"),
        'current_date': datetime.now().strftime("%Y-%m-%d"),
        'user_goal': getattr(user_details, 'goal', 'maintain')
    }
    return render(request, 'workouts.html', context)