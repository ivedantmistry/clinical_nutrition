# meals/serializers.py

from rest_framework import serializers
from .models import Meal, MealIngredient

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = "__all__"

class MealIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealIngredient
        fields = "__all__"
        