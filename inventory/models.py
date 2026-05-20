# inventory/models.py
from django.db import models
from django.conf import settings


class Inventory(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class MasterItemInfo(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True)
    potassium_mg = models.FloatField(null=True)
    protein_g = models.FloatField(null=True)
    total_sugar_g = models.FloatField(null=True)
    added_sugar_g = models.FloatField(null=True)
    sodium_g = models.FloatField(null=True)
    quantity_g = models.FloatField(null=True)
    calories = models.FloatField(null=True)


class PantryItem(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    master_item_info = models.ForeignKey(MasterItemInfo, on_delete=models.CASCADE)
    quantity_g = models.FloatField(null=True)
