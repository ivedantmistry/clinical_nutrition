# meals/views.py

from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from .models import Meal, MealIngredient
from inventory.models import PantryItem
from django.db import transaction
from .serializers import MealSerializer, MealIngredientSerializer
from rest_framework.permissions import IsAuthenticated


class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Meal.objects.filter(user=self.request.user)


class MealIngredientViewSet(viewsets.ModelViewSet):
    serializer_class = MealIngredientSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        with transaction.atomic():

            ingredient_data = serializer.validated_data
            requested_quantity = ingredient_data["quantity_used_g"]
            master_item = ingredient_data["master_item_info"]
            meal = ingredient_data["meal"]

            pantry_item = PantryItem.objects.filter(
                inventory__user=meal.user, master_item_info=master_item
            ).first()

            if not pantry_item:
                raise ValidationError(
                    f"You do not have {master_item.name} in your inventory."
                )

            if pantry_item.quantity_g < requested_quantity:
                raise ValidationError(
                    f"Not enough {master_item.name}. You requested {requested_quantity}g but only have {pantry_item.quantity_g}g."
                )

            pantry_item.quantity_g -= requested_quantity
            pantry_item.save()

            serializer.save()

    def get_queryset(self):
        return MealIngredient.objects.filter(meal__user=self.request.user)