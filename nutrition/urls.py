from django.urls import path
from . import views

urlpatterns = [
    path('', views.nutrition_view, name='nutrition'),
    path('api/user-details/', views.api_user_details, name='api_user_details'),
    path('api/calculate-calories/', views.api_calculate_calories, name='api_calculate_calories'),
    path('api/save-meal/', views.api_save_meal, name='api_save_meal'),
    path('api/get-meals/', views.api_get_meals, name='api_get_meals'),
    path('api/get-nutrition-data/', views.api_get_nutrition_data, name='api_get_nutrition_data'),
]