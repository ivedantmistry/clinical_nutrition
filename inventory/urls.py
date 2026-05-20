# inventory/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryViewSet, MasterItemInfoViewset, PantryItemViewSet

router = DefaultRouter()

router.register(r'inventories', InventoryViewSet)
router.register(r'masteriteminfo',MasterItemInfoViewset)
router.register(r'pantryitem',PantryItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]