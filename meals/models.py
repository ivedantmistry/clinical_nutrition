# meals/models.py
from django.db import models
from django.conf import settings
from inventory.models import MasterItemInfo


class Meal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    ingredients = models.ManyToManyField(MasterItemInfo, through='MealIngredient')

    def total_meal_potassium(self):
        total = 0.0
        for ingredient in self.mealingredient_set.all():
            total += ingredient.calculate_potassium()
        return total
    
    def total_meal_sodium(self):
        total = 0.0
        for ingredient in self.mealingredient_set.all():
            total += ingredient.calculate_sodium()
        return total
    
    def total_meal_protein(self):
        total = 0.0
        for ingredient in self.mealingredient_set.all():
            total += ingredient.calculate_protein()
        return total
    
    def total_meal_calories(self):
        total = 0.0
        for ingredient in self.mealingredient_set.all():
            total += ingredient.calculate_calories()
        return total
    
    def total_meal_sugar(self):
        total = 0.0
        for ingredient in self.mealingredient_set.all():
            total += ingredient.calculate_total_sugar()
        return total
    

class MealIngredient(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity_used_g = models.FloatField()
    master_item_info = models.ForeignKey(MasterItemInfo, on_delete=models.CASCADE)

    def calculate_potassium(self):
        if not self.quantity_used_g or not self.master_item_info.quantity_g or not self.master_item_info.potassium_mg:
            return 0.0
        ratio = self.quantity_used_g / self.master_item_info.quantity_g
        return ratio * self.master_item_info.potassium_mg
    
    def calculate_sodium(self):
        if not self.quantity_used_g or not self.master_item_info.quantity_g or not self.master_item_info.sodium_g:
            return 0.0
        ratio = self.quantity_used_g / self.master_item_info.quantity_g
        return ratio * self.master_item_info.sodium_g
    
    def calculate_protein(self):
        if not self.quantity_used_g or not self.master_item_info.quantity_g or not self.master_item_info.protein_g:
            return 0.0
        ratio = self.quantity_used_g / self.master_item_info.quantity_g
        return ratio * self.master_item_info.protein_g
    
    def calculate_calories(self):
        if not self.quantity_used_g or not self.master_item_info.quantity_g or not self.master_item_info.calories:
            return 0.0
        ratio = self.quantity_used_g / self.master_item_info.quantity_g
        return ratio * self.master_item_info.calories
    
    def calculate_total_sugar(self):
        if not self.quantity_used_g or not self.master_item_info.quantity_g or not self.master_item_info.total_sugar_g:
            return 0.0
        ratio = self.quantity_used_g / self.master_item_info.quantity_g
        return ratio * self.master_item_info.total_sugar_g
    