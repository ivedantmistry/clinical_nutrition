# meals/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MealIngredientViewSet, MealViewSet

router = DefaultRouter()

router.register(r'meals',MealViewSet)
router.register(r'mealingredient',MealIngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]