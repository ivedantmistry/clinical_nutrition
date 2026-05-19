# meals/models.py
from django.db import models
from django.conf import settings
from inventory.models import MasterItemInfo


class Meal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    ingredients = models.ManyToManyField(MasterItemInfo, through='MealIngredient')


class MealIngredient(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity_used_g = models.IntegerField()
    master_item_info = models.ForeignKey(MasterItemInfo, on_delete=models.CASCADE)
