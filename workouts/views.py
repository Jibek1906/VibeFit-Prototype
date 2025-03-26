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
    """API for selecting workouts based on user level, goal, and AI-generated plan."""
    try:
        user_details = UserDetails.objects.get(user=request.user)
    except UserDetails.DoesNotExist:
        return JsonResponse({"error": "User details not found"}, status=400)

    # Generate personalized workout plan based on user details
    workout_plan = generate_workout_plan(user_details)

    # Search YouTube for workout videos based on the plan
    youtube_workouts = []
    for workout_name in workout_plan:
        youtube_videos = search_youtube_videos(workout_name, max_results=5)  # Fetch videos for each workout
        youtube_workouts.extend(youtube_videos)

    if not youtube_workouts:
        return JsonResponse({"error": "No workouts found"}, status=400)

    # Select a random workout video for the day
    selected_workouts = random.sample(youtube_workouts, min(len(youtube_workouts), 3))  # Limit to 3 videos

    # Generate JSON response for workout schedule
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

def generate_workout_plan(user_details):
    """Generates a personalized workout plan based on user data."""
    workouts = []

    # Example: A simple heuristic to generate workout plans
    if user_details.goal == 'lose-weight':
        if user_details.training_level == 'beginner':
            workouts = ['Cardio: Walking', 'Strength: Bodyweight Squats']
        elif user_details.training_level == 'intermediate':
            workouts = ['Cardio: Running', 'Strength: Dumbbell Exercises']
        else:
            workouts = ['HIIT Cardio', 'Strength: Compound Lifts']

    elif user_details.goal == 'gain-muscle':
        if user_details.training_level == 'beginner':
            workouts = ['Strength: Bodyweight Squats', 'Strength: Push-ups']
        elif user_details.training_level == 'intermediate':
            workouts = ['Strength: Deadlifts', 'Strength: Pull-ups']
        else:
            workouts = ['Strength: Powerlifting', 'Strength: Olympic Lifts']

    # Add more custom logic here for other goals and levels

    return workouts

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