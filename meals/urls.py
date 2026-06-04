from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MealIngredientViewSet, MealViewSet

router = DefaultRouter()

router.register(r'meals', MealViewSet, basename='meal')
router.register(r'mealingredient', MealIngredientViewSet, basename='mealingredient')

urlpatterns = [
    path('', include(router.urls)),
]