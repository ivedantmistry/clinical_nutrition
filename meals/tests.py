# meals/tests.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from inventory.models import Inventory, MasterItemInfo, PantryItem
from meals.models import Meal, MealIngredient
from organizations.models import Organization, OrganizationMember

User = get_user_model()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_user(username="testuser", password="testpass123"):
    return User.objects.create_user(username=username, password=password)


def make_org(name="Test Clinic"):
    return Organization.objects.create(name=name)


def make_food(**kwargs):
    """Banana raw as default — real values from your BLS data."""
    defaults = dict(
        name="Banana raw",
        potassium_mg=334.0,
        protein_g=1.319,
        total_sugar_g=13.89,
        sodium_g=0.00052,
        quantity_g=100.0,
        calories=79.0,
    )
    defaults.update(kwargs)
    return MasterItemInfo.objects.create(**defaults)


def setup_user_with_inventory(username="testuser"):
    """Create user + org + inventory. Returns (user, org, inventory)."""
    user = make_user(username=username)
    org = make_org()
    OrganizationMember.objects.create(user=user, organization=org)
    inventory = Inventory.objects.create(user=user, organization=org)
    return user, org, inventory


def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


# ---------------------------------------------------------------------------
# MealIngredient nutrient calculation tests
# — these are the most critical tests in the whole project
# ---------------------------------------------------------------------------


class NutrientCalculationTest(TestCase):
    """
    Tests the proportional nutrient math in MealIngredient.
    All values are per 100g in MasterItemInfo, scaled by quantity_used_g.
    """

    def setUp(self):
        self.user, self.org, self.inventory = setup_user_with_inventory()
        self.food = make_food(
            name="Banana raw",
            potassium_mg=334.0,  # per 100g
            protein_g=1.319,
            total_sugar_g=13.89,
            sodium_g=0.00052,
            quantity_g=100.0,
            calories=79.0,
        )
        self.meal = Meal.objects.create(
            user=self.user,
            organization=self.org,
            name="Test meal",
        )

    def _make_ingredient(self, quantity_used_g):
        return MealIngredient(
            meal=self.meal,
            master_item_info=self.food,
            quantity_used_g=quantity_used_g,
        )

    def test_potassium_at_100g_equals_base_value(self):
        ingredient = self._make_ingredient(100.0)
        self.assertAlmostEqual(ingredient.calculate_potassium(), 334.0, places=2)

    def test_potassium_at_50g_is_half(self):
        ingredient = self._make_ingredient(50.0)
        self.assertAlmostEqual(ingredient.calculate_potassium(), 167.0, places=2)

    def test_potassium_at_200g_is_double(self):
        ingredient = self._make_ingredient(200.0)
        self.assertAlmostEqual(ingredient.calculate_potassium(), 668.0, places=2)

    def test_sodium_calculation(self):
        ingredient = self._make_ingredient(100.0)
        self.assertAlmostEqual(ingredient.calculate_sodium(), 0.00052, places=5)

    def test_protein_calculation(self):
        ingredient = self._make_ingredient(100.0)
        self.assertAlmostEqual(ingredient.calculate_protein(), 1.319, places=3)

    def test_calories_calculation(self):
        ingredient = self._make_ingredient(100.0)
        self.assertAlmostEqual(ingredient.calculate_calories(), 79.0, places=1)

    def test_sugar_calculation(self):
        ingredient = self._make_ingredient(100.0)
        self.assertAlmostEqual(ingredient.calculate_total_sugar(), 13.89, places=2)

    def test_null_potassium_returns_zero(self):
        food = make_food(name="Unknown", potassium_mg=None)
        ingredient = MealIngredient(
            meal=self.meal,
            master_item_info=food,
            quantity_used_g=100.0,
        )
        self.assertEqual(ingredient.calculate_potassium(), 0.0)

    def test_null_sodium_returns_zero(self):
        food = make_food(name="Unknown2", sodium_g=None)
        ingredient = MealIngredient(
            meal=self.meal,
            master_item_info=food,
            quantity_used_g=100.0,
        )
        self.assertEqual(ingredient.calculate_sodium(), 0.0)

    def test_zero_quantity_returns_zero_potassium(self):
        ingredient = self._make_ingredient(0.0)
        self.assertEqual(ingredient.calculate_potassium(), 0.0)


# ---------------------------------------------------------------------------
# Meal model total calculation tests
# ---------------------------------------------------------------------------


class MealTotalCalculationTest(TestCase):
    """
    Tests that Meal.total_meal_* aggregates correctly across ingredients.
    """

    def setUp(self):
        self.user, self.org, self.inventory = setup_user_with_inventory()
        self.food_a = make_food(
            name="Banana raw",
            potassium_mg=334.0,
            protein_g=1.319,
            total_sugar_g=13.89,
            sodium_g=0.00052,
            quantity_g=100.0,
            calories=79.0,
        )
        self.food_b = make_food(
            name="Spinach raw",
            potassium_mg=573.0,
            protein_g=2.067,
            total_sugar_g=0.75,
            sodium_g=0.05,
            quantity_g=100.0,
            calories=18.0,
        )
        self.meal = Meal.objects.create(
            user=self.user,
            organization=self.org,
            name="Mixed meal",
        )
        # 100g banana + 50g spinach
        MealIngredient.objects.create(
            meal=self.meal,
            master_item_info=self.food_a,
            quantity_used_g=100.0,
        )
        MealIngredient.objects.create(
            meal=self.meal,
            master_item_info=self.food_b,
            quantity_used_g=50.0,
        )

    def test_total_potassium_sums_ingredients(self):
        # 100g banana = 334mg K, 50g spinach = 286.5mg K
        expected = 334.0 + (573.0 * 0.5)
        self.assertAlmostEqual(self.meal.total_meal_potassium(), expected, places=1)

    def test_total_calories_sums_ingredients(self):
        # 100g banana = 79 kcal, 50g spinach = 9 kcal
        expected = 79.0 + (18.0 * 0.5)
        self.assertAlmostEqual(self.meal.total_meal_calories(), expected, places=1)

    def test_total_sodium_sums_ingredients(self):
        expected = 0.00052 + (0.05 * 0.5)
        self.assertAlmostEqual(self.meal.total_meal_sodium(), expected, places=5)

    def test_empty_meal_returns_zeros(self):
        empty_meal = Meal.objects.create(
            user=self.user,
            organization=self.org,
            name="Empty meal",
        )
        self.assertEqual(empty_meal.total_meal_potassium(), 0.0)
        self.assertEqual(empty_meal.total_meal_calories(), 0.0)
        self.assertEqual(empty_meal.total_meal_sodium(), 0.0)
        self.assertEqual(empty_meal.total_meal_protein(), 0.0)
        self.assertEqual(empty_meal.total_meal_sugar(), 0.0)


# ---------------------------------------------------------------------------
# Meal API tests
# ---------------------------------------------------------------------------


class MealAPITest(TestCase):

    def setUp(self):
        self.user, self.org, self.inventory = setup_user_with_inventory()
        self.other_user, _, _ = setup_user_with_inventory(username="otheruser")
        self.client = auth_client(self.user)
        # meal belonging to other user — should never appear in self.user's responses
        Meal.objects.create(
            user=self.other_user,
            organization=self.org,
            name="Other user's meal",
        )

    def test_create_meal(self):
        response = self.client.post(
            "/api/meals/meals/",
            {
                "name": "Breakfast",
                "organization": self.org.id,
                "user": self.user.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Meal.objects.filter(user=self.user).count(), 1)

    def test_list_meals_returns_only_own(self):
        Meal.objects.create(user=self.user, organization=self.org, name="My meal")
        response = self.client.get("/api/meals/meals/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [m["id"] for m in response.data["results"]]
        # other user's meal must not appear
        other_meal_ids = Meal.objects.filter(user=self.other_user).values_list(
            "id", flat=True
        )
        for other_id in other_meal_ids:
            self.assertNotIn(other_id, names)

    def test_unauthenticated_blocked(self):
        response = APIClient().get("/api/meals/meals/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ---------------------------------------------------------------------------
# MealIngredient API + pantry deduction tests
# — this is the most important business logic in the whole project
# ---------------------------------------------------------------------------


class MealIngredientAPITest(TestCase):

    def setUp(self):
        self.user, self.org, self.inventory = setup_user_with_inventory()
        self.food = make_food()
        self.meal = Meal.objects.create(
            user=self.user,
            organization=self.org,
            name="Lunch",
        )
        # stock the pantry with 500g of banana
        self.pantry_item = PantryItem.objects.create(
            inventory=self.inventory,
            master_item_info=self.food,
            quantity_g=500.0,
        )
        self.client = auth_client(self.user)

    def test_adding_ingredient_deducts_from_pantry(self):
        self.client.post(
            "/api/meals/mealingredient/",
            {
                "meal": self.meal.id,
                "master_item_info": self.food.id,
                "quantity_used_g": 150.0,
            },
        )
        self.pantry_item.refresh_from_db()
        self.assertAlmostEqual(self.pantry_item.quantity_g, 350.0, places=2)

    def test_adding_ingredient_creates_meal_ingredient(self):
        response = self.client.post(
            "/api/meals/mealingredient/",
            {
                "meal": self.meal.id,
                "master_item_info": self.food.id,
                "quantity_used_g": 100.0,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MealIngredient.objects.count(), 1)

    def test_requesting_more_than_pantry_fails(self):
        response = self.client.post(
            "/api/meals/mealingredient/",
            {
                "meal": self.meal.id,
                "master_item_info": self.food.id,
                "quantity_used_g": 600.0,  # only 500g in pantry
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Not enough", str(response.data))

    def test_requesting_item_not_in_pantry_fails(self):
        other_food = make_food(name="Avocado raw", potassium_mg=550.0)
        response = self.client.post(
            "/api/meals/mealingredient/",
            {
                "meal": self.meal.id,
                "master_item_info": other_food.id,
                "quantity_used_g": 50.0,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("do not have", str(response.data))

    def test_pantry_not_deducted_on_failed_request(self):
        """Atomic transaction — pantry must be unchanged if validation fails."""
        self.client.post(
            "/api/meals/mealingredient/",
            {
                "meal": self.meal.id,
                "master_item_info": self.food.id,
                "quantity_used_g": 9999.0,  # will fail
            },
        )
        self.pantry_item.refresh_from_db()
        self.assertAlmostEqual(self.pantry_item.quantity_g, 500.0, places=2)

    def test_response_includes_calculated_nutrients(self):
        response = self.client.post(
            "/api/meals/mealingredient/",
            {
                "meal": self.meal.id,
                "master_item_info": self.food.id,
                "quantity_used_g": 100.0,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("calculated_potassium", response.data)
        self.assertAlmostEqual(
            float(response.data["calculated_potassium"]),
            334.0,
            places=1,
        )

    def test_unauthenticated_blocked(self):
        response = APIClient().post("/api/meals/mealingredient/", {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
