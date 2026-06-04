# meals/serializers.py

from rest_framework import serializers
from .models import Meal, MealIngredient


class MealIngredientSerializer(serializers.ModelSerializer):
    calculated_potassium = serializers.ReadOnlyField(source="calculate_potassium")
    calculated_sodium = serializers.ReadOnlyField(source="calculate_sodium")
    calculated_protein = serializers.ReadOnlyField(source="calculate_protein")
    calculated_calories = serializers.ReadOnlyField(source="calculate_calories")
    calculated_sugar = serializers.ReadOnlyField(source="calculate_total_sugar")

    class Meta:
        model = MealIngredient
        fields = [
            "id",
            "meal",
            "master_item_info",
            "quantity_used_g",
            "calculated_potassium",
            "calculated_sodium",
            "calculated_protein",
            "calculated_sugar",
            "calculated_calories",
        ]


class MealSerializer(serializers.ModelSerializer):
    total_potassium = serializers.ReadOnlyField(source="total_meal_potassium")
    total_sodium = serializers.ReadOnlyField(source="total_meal_sodium")
    total_sugar = serializers.ReadOnlyField(source="total_meal_sugar")
    total_protein = serializers.ReadOnlyField(source="total_meal_protein")
    total_calories = serializers.ReadOnlyField(source="total_meal_calories")
    ingredients_list = MealIngredientSerializer(
        source="mealingredient_set", many=True, read_only=True
    )

    class Meta:
        model = Meal
        fields = [
            "id",
            "created_at",
            "total_potassium",
            "ingredients_list",
            "total_sodium",
            "total_sugar",
            "total_protein",
            "total_calories",
        ]
