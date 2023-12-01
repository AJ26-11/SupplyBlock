from django.test import TestCase, Client
from django.urls import reverse
from .models import CoffeeBeanBatch
from django.contrib.auth.models import User

class CoffeeBeanBatchModelTests(TestCase):

    def setUp(self):
        CoffeeBeanBatch.objects.create(
            batch_id="batch123",
            farm_name="Test Farm",
            origin_country="Testland",
            harvest_date="2021-01-01",
            # ... other fields ...
        )

