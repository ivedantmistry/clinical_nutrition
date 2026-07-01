# meals/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MealIngredientViewSet, MealViewSet

meal_router = DefaultRouter()
meal_router.register(r"", MealViewSet, basename="meal")

ingredient_router = DefaultRouter()
ingredient_router.register(r"", MealIngredientViewSet, basename="meal-ingredient")

urlpatterns = [
    path("", include(meal_router.urls)),
]

ingredient_urlpatterns = [
    path("", include(ingredient_router.urls)),
]
