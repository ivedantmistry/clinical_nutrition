# inventory/tests.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from inventory.models import Inventory, MasterItemInfo, PantryItem
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
    defaults = dict(
        name="Banana raw",
        potassium_mg=334.0,
        protein_g=1.319,
        total_sugar_g=13.89,
        sodium_g=0.00052,
        quantity_g=100.0,
        calories=79,
    )
    defaults.update(kwargs)
    return MasterItemInfo.objects.create(**defaults)


def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


# ---------------------------------------------------------------------------
# MasterItemInfo model tests
# ---------------------------------------------------------------------------


class MasterItemInfoModelTest(TestCase):

    def test_str_returns_name(self):
        food = make_food(name="Spinach raw")
        self.assertEqual(str(food), "Spinach raw")

    def test_nullable_fields_allowed(self):
        food = MasterItemInfo.objects.create(
            name="Mystery food",
            quantity_g=100.0,
            potassium_mg=None,
            sodium_g=None,
            calories=None,
        )
        self.assertIsNone(food.potassium_mg)
        self.assertIsNone(food.sodium_g)

    def test_brand_defaults_blank(self):
        food = make_food()
        self.assertEqual(food.brand, "")


# ---------------------------------------------------------------------------
# Inventory model tests
# ---------------------------------------------------------------------------


class InventoryModelTest(TestCase):

    def setUp(self):
        self.user = make_user()
        self.org = make_org()
        OrganizationMember.objects.create(user=self.user, organization=self.org)
        self.inventory = Inventory.objects.create(user=self.user, organization=self.org)

    def test_str_contains_username_and_org(self):
        s = str(self.inventory)
        self.assertIn(self.user.username, s)
        self.assertIn(self.org.name, s)

    def test_one_inventory_per_user(self):
        # OneToOneField — creating a second must raise
        with self.assertRaises(Exception):
            Inventory.objects.create(user=self.user, organization=self.org)


# ---------------------------------------------------------------------------
# PantryItem model tests
# ---------------------------------------------------------------------------


class PantryItemModelTest(TestCase):

    def setUp(self):
        self.user = make_user()
        self.org = make_org()
        OrganizationMember.objects.create(user=self.user, organization=self.org)
        self.inventory = Inventory.objects.create(user=self.user, organization=self.org)
        self.food = make_food()

    def test_str_contains_quantity_and_name(self):
        item = PantryItem.objects.create(
            inventory=self.inventory,
            master_item_info=self.food,
            quantity_g=250.0,
        )
        self.assertIn("250.0", str(item))
        self.assertIn(self.food.name, str(item))

    def test_quantity_can_be_null(self):
        item = PantryItem.objects.create(
            inventory=self.inventory,
            master_item_info=self.food,
            quantity_g=None,
        )
        self.assertIsNone(item.quantity_g)


# ---------------------------------------------------------------------------
# Inventory API tests
# ---------------------------------------------------------------------------


class InventoryAPITest(TestCase):

    def setUp(self):
        self.user = make_user()
        self.other_user = make_user(username="otheruser")
        self.org = make_org()
        OrganizationMember.objects.create(user=self.user, organization=self.org)
        OrganizationMember.objects.create(user=self.other_user, organization=self.org)
        self.inventory = Inventory.objects.create(user=self.user, organization=self.org)
        Inventory.objects.create(user=self.other_user, organization=self.org)
        self.client = auth_client(self.user)

    def test_list_returns_only_own_inventory(self):
        response = self.client.get("/api/inventory/inventories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # user should only see their own
        ids = [i["id"] for i in response.data["results"]]
        self.assertEqual(ids, [self.inventory.id])

    def test_unauthenticated_request_rejected(self):
        response = APIClient().get("/api/inventory/inventories/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ---------------------------------------------------------------------------
# MasterItemInfo API tests
# ---------------------------------------------------------------------------


class FoodAPITest(TestCase):

    def setUp(self):
        self.user = make_user()
        self.client = auth_client(self.user)
        self.food = make_food()

    def test_list_foods(self):
        response = self.client.get("/api/inventory/masteriteminfo/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data["count"], 1)

    def test_retrieve_single_food(self):
        response = self.client.get(f"/api/inventory/masteriteminfo/{self.food.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.food.name)

    def test_unauthenticated_blocked(self):
        response = APIClient().get("/api/inventory/masteriteminfo/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ---------------------------------------------------------------------------
# PantryItem API tests
# ---------------------------------------------------------------------------


class PantryItemAPITest(TestCase):

    def setUp(self):
        self.user = make_user()
        self.org = make_org()
        OrganizationMember.objects.create(user=self.user, organization=self.org)
        self.inventory = Inventory.objects.create(user=self.user, organization=self.org)
        self.food = make_food()
        self.client = auth_client(self.user)

    def test_create_pantry_item(self):
        response = self.client.post(
            "/api/inventory/pantryitem/",
            {
                "inventory": self.inventory.id,
                "master_item_info": self.food.id,
                "quantity_g": 500.0,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PantryItem.objects.count(), 1)

    def test_list_pantry_items(self):
        PantryItem.objects.create(
            inventory=self.inventory,
            master_item_info=self.food,
            quantity_g=200.0,
        )
        response = self.client.get("/api/inventory/pantryitem/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_pantry_item(self):
        item = PantryItem.objects.create(
            inventory=self.inventory,
            master_item_info=self.food,
            quantity_g=100.0,
        )
        response = self.client.delete(f"/api/inventory/pantryitem/{item.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PantryItem.objects.count(), 0)
