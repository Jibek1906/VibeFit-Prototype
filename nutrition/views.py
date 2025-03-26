from django.shortcuts import render
from .models import CaloricIntake

def calculate_calories(request):
    if request.method == 'POST':
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        training_level = request.POST.get('training_level')
        goal = request.POST.get('goal')

        caloric_intake, created = CaloricIntake.objects.get_or_create(user=request.user.userdetails)
        caloric_intake.calculate_calories()

        return render(request, 'nutrition.html', {'caloric_intake': caloric_intake})
    else:
        return render(request, 'nutrition.html')
