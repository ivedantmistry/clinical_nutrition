# meals/views.py

from rest_framework import viewsets
from .models import Meal, MealIngredient
from .serializers import MealSerializer, MealIngredientSerializer
from rest_framework.permissions import IsAuthenticated


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]


class MealIngredientViewSet(viewsets.ModelViewSet):
    queryset = MealIngredient.objects.all()
    serializer_class = MealIngredientSerializer
    permission_classes = [IsAuthenticated]
