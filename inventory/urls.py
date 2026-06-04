from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryViewSet, MasterItemInfoViewset, PantryItemViewSet

router = DefaultRouter()
router.register(r'inventories', InventoryViewSet, basename='inventory')
router.register(r'masteriteminfo', MasterItemInfoViewset, basename='masteriteminfo')
router.register(r'pantryitem', PantryItemViewSet, basename='pantryitem')

urlpatterns = [
    path('', include(router.urls)),
]