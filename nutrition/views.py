from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import DailyNutrition, Meal
from users.models import UserDetails
import json
from django.views.decorators.csrf import csrf_exempt

# nutrition/views.py

@login_required
def calculate_daily_calories(user_details):
    # Рассчитываем возраст
    age = (datetime.now().date() - user_details.birth_date).days // 365 if user_details.birth_date else 30
    weight = float(user_details.weight)
    height = user_details.height

    # Расчет базового метаболизма (BMR) по формуле Миффлина-Сан Жеора
    if user_details.gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:  # female
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Учет уровня активности
    activity_multipliers = {
        'beginner': 1.2,
        'intermediate': 1.375,
        'advanced': 1.55
    }
    activity_multiplier = activity_multipliers.get(user_details.training_level, 1.2)
    tdee = bmr * activity_multiplier  # Total Daily Energy Expenditure

    # Корректировка по цели
    if user_details.goal == 'lose-weight':
        calories = tdee * 0.85  # 15% дефицит
    elif user_details.goal == 'gain-muscle':
        calories = tdee * 1.15  # 15% профицит
    else:  # maintain
        calories = tdee

    # Распределение макронутриентов
    if user_details.goal == 'gain-muscle':
        proteins = weight * 2.2  # 2.2г на кг веса для набора мышц
        fats = weight * 1  # 1г на кг веса
    else:
        proteins = weight * 1.6  # 1.6г на кг веса стандарт
        fats = weight * 0.8  # 0.8г на кг веса

    carbs = (calories - (proteins * 4 + fats * 9)) / 4  # остаток калорий на углеводы

    return {
        'calories': round(calories),
        'proteins': round(proteins),
        'fats': round(fats),
        'carbs': round(carbs)
    }

@login_required
def nutrition_view(request):
    user_details = UserDetails.objects.get(user=request.user)
    today = datetime.now().date()

    try:
        daily_nutrition = DailyNutrition.objects.get(user=user_details, date=today)
    except DailyNutrition.DoesNotExist:
        # Сначала создаем запись с нулевыми значениями
        daily_nutrition = DailyNutrition.objects.create(
            user=user_details,
            date=today,
            calories=0,
            proteins=0,
            fats=0,
            carbs=0
        )
        # Затем обновляем расчетными значениями
        calculated = calculate_daily_calories(user_details)
        for field, value in calculated.items():
            setattr(daily_nutrition, field, value)
        daily_nutrition.save()

    meals = Meal.objects.filter(nutrition=daily_nutrition).order_by('meal_type')
    remaining_calories = daily_nutrition.calories - sum(m.calories for m in meals)

    context = {
        'daily_nutrition': daily_nutrition,
        'meals': meals,
        'remaining_calories': remaining_calories,
    }
    return render(request, 'nutrition.html', context)

@login_required
@csrf_exempt
def api_save_meal(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_details = UserDetails.objects.get(user=request.user)
            
            # Получаем или создаем запись о питании за день
            date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            daily_nutrition, created = DailyNutrition.objects.get_or_create(
                user=user_details,
                date=date,
                defaults={
                    'calories': 0,
                    'proteins': 0,
                    'fats': 0,
                    'carbs': 0
                }
            )
            
            # Создаем прием пищи
            meal = Meal.objects.create(
                nutrition=daily_nutrition,
                meal_type=data['meal_type'],
                name=data['name'],
                calories=data['calories'],
                proteins=data['proteins'],
                fats=data['fats'],
                carbs=data['carbs']
            )
            
            # Обновляем суммарные значения за день
            daily_nutrition.calories += data['calories']
            daily_nutrition.proteins += data['proteins']
            daily_nutrition.fats += data['fats']
            daily_nutrition.carbs += data['carbs']
            daily_nutrition.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Meal saved successfully'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'error': str(e)
            }, status=400)
    return JsonResponse({
        'status': 'error',
        'error': 'Invalid request method'
    }, status=405)

@login_required
@csrf_exempt
def api_get_meals(request):
    if request.method == 'GET':
        try:
            user_details = UserDetails.objects.get(user=request.user)
            date_from = request.GET.get('date_from')
            date_to = request.GET.get('date_to')
            
            if not date_from or not date_to:
                return JsonResponse({
                    'status': 'error',
                    'error': 'Missing date parameters'
                }, status=400)
                
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            
            daily_nutritions = DailyNutrition.objects.filter(
                user=user_details,
                date__range=[date_from, date_to]
            ).prefetch_related('meals')
            
            meals_data = []
            for nutrition in daily_nutritions:
                for meal in nutrition.meals.all():
                    meals_data.append({
                        'date': nutrition.date.strftime('%Y-%m-%d'),
                        'meal_type': meal.meal_type,
                        'name': meal.name,
                        'calories': meal.calories,
                        'proteins': meal.proteins,
                        'fats': meal.fats,
                        'carbs': meal.carbs
                    })
                    
            return JsonResponse({
                'status': 'success',
                'meals': meals_data
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'error': str(e)
            }, status=400)
    return JsonResponse({
        'status': 'error',
        'error': 'Invalid request method'
    }, status=405)

@login_required
@csrf_exempt
def api_user_details(request):
    if request.method == 'GET':
        try:
            user_details = UserDetails.objects.get(user=request.user)
            return JsonResponse({
                'weight': float(user_details.weight),
                'height': user_details.height,
                'training_level': user_details.training_level,
                'goal': user_details.goal,
                'gender': user_details.gender,
                'age': (datetime.now().date() - user_details.birth_date).days // 365 if user_details.birth_date else 30,
                'status': 'success'
            })
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 'error'}, status=400)
    return JsonResponse({'error': 'Invalid request method', 'status': 'error'}, status=405)

@login_required
@csrf_exempt
def api_calculate_calories(request):
    if request.method == 'POST':
        try:
            user_details = UserDetails.objects.get(user=request.user)
            data = calculate_daily_calories(user_details)
            return JsonResponse({
                'daily_calorie_goal': data['calories'],
                'proteins': data['proteins'],
                'fats': data['fats'],
                'carbs': data['carbs'],
                'status': 'success'
            })
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 'error'}, status=400)
    return JsonResponse({'error': 'Invalid request method', 'status': 'error'}, status=405)

# nutrition/views.py

@login_required
def api_get_nutrition_data(request):
    if request.method == 'GET':
        try:
            user_details = UserDetails.objects.get(user=request.user)
            date_from = request.GET.get('date_from', datetime.now().date().strftime('%Y-%m-%d'))
            date_to = request.GET.get('date_to', datetime.now().date().strftime('%Y-%m-%d'))

            daily_nutritions = DailyNutrition.objects.filter(
                user=user_details,
                date__range=[date_from, date_to]
            ).prefetch_related('meals')

            days_data = []
            for nutrition in daily_nutritions:
                days_data.append({
                    'date': nutrition.date.strftime('%Y-%m-%d'),
                    'day': nutrition.date.strftime('%A').lower(),
                    'calories': nutrition.calories,
                    'proteins': nutrition.proteins,
                    'fats': nutrition.fats,
                    'carbs': nutrition.carbs,
                    'goal_calories': calculate_daily_calories(user_details)['calories'],
                    'meals': [{
                        'meal_type': meal.meal_type,
                        'name': meal.name,
                        'calories': meal.calories,
                        'proteins': meal.proteins,
                        'fats': meal.fats,
                        'carbs': meal.carbs
                    } for meal in nutrition.meals.all()]
                })

            return JsonResponse({
                'status': 'success',
                'days': days_data
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'error': str(e)
            }, status=400)
    return JsonResponse({
        'status': 'error',
        'error': 'Invalid request method'
    }, status=405)