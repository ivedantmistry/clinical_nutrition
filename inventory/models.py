# inventory/models.py
from django.db import models
from django.conf import settings


class Inventory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class MasterItemInfo(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True)
    potassium_mg = models.IntegerField()
    protein_g = models.IntegerField()
    sugar_g = models.IntegerField()


class PantryItem(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    master_item_info = models.ForeignKey(MasterItemInfo, on_delete=models.CASCADE)
    quantity_g = models.IntegerField()
