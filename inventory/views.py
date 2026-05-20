# inventory/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Inventory, MasterItemInfo, PantryItem
from .serializers import (
    InventorySerializer,
    MasterItemInfoSerializer,
    PantryItemSerializer,
)


class InventoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class MasterItemInfoViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = MasterItemInfo.objects.all()
    serializer_class = MasterItemInfoSerializer


class PantryItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PantryItem.objects.all()
    serializer_class = PantryItemSerializer
