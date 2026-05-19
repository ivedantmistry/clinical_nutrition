# inventory/serializers.py
from rest_framework import serializers
from .models import Inventory, MasterItemInfo, PantryItem


class MasterItemInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterItemInfo
        fields = "__all__"


class PantryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PantryItem
        fields = "__all__"


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"
