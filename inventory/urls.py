# inventory/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryViewSet, MasterItemInfoViewset, PantryItemViewSet

router = DefaultRouter()
router.register(r"", InventoryViewSet, basename="inventory")

food_router = DefaultRouter()
food_router.register(r"", MasterItemInfoViewset, basename="food")

pantry_router = DefaultRouter()
pantry_router.register(r"", PantryItemViewSet, basename="pantry")

urlpatterns = [
    path("", include(router.urls)),
]

food_urlpatterns = [
    path("", include(food_router.urls)),
]

pantry_urlpatterns = [
    path("", include(pantry_router.urls)),
]
