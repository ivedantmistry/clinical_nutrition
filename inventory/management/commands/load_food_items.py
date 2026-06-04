import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from inventory.models import MasterItemInfo 

class Command(BaseCommand):
    help = 'Loads the BLS food data from JSON into the MasterItemInfo table'

    def handle(self, *args, **kwargs):
        # Path to your JSON file (assuming it's in the same folder as manage.py)
        file_path = os.path.join(settings.BASE_DIR, 'master_item_info.json')

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Could not find {file_path}"))
            return

        self.stdout.write("Loading data... this might take a few seconds.")

        # Create a list to hold all our model instances
        items_to_create = []

        for item in data:
            items_to_create.append(
                MasterItemInfo(
                    # Truncating name to 255 chars just in case some are super long
                    name=str(item.get('name', ''))[:255], 
                    brand=item.get('brand', ''),
                    potassium_mg=item.get('potassium_mg'),
                    protein_g=item.get('protein_g'),
                    total_sugar_g=item.get('total_sugar_g'),
                    added_sugar_g=item.get('added_sugar_g'),
                    sodium_g=item.get('sodium_g'),
                    quantity_g=item.get('quantity_g'),
                    calories=item.get('calories')
                )
            )

        # Clear the existing table to avoid duplicates if you run this multiple times
        MasterItemInfo.objects.all().delete()

        # bulk_create is much faster than calling .save() 9000 times
        MasterItemInfo.objects.bulk_create(items_to_create, batch_size=1000)

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(items_to_create)} food items!'))