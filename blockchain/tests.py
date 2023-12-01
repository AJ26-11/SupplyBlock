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

    def test_batch_creation(self):
        batch = CoffeeBeanBatch.objects.get(batch_id="batch123")
        self.assertEqual(batch.farm_name, "Test Farm")

    def test_batch_failure(self):
        # This test is supposed to fail for demonstration
        batch = CoffeeBeanBatch.objects.get(batch_id="batch123")
        self.assertEqual(batch.farm_name, "Nonexistent Farm")

class UserRegistrationViewTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_registration_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_successful_registration(self):
        response = self.client.post(reverse('register'), data={
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect status
        self.assertEqual(User.objects.count(), 1)

class UserLoginViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        response = self.client.post(reverse('login'), data={
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect status

    def test_failed_login(self):
        response = self.client.post(reverse('login'), data={
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertNotEqual(response.status_code,302)
