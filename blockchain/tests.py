from django.test import TestCase, Client
from django.urls import reverse
from .models import Batch
from unittest.mock import patch

class MockTransactionHash:
    def hex(self):
        return '0x123'

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.add_batch_url = reverse('add_batch')
        self.view_batch_url = reverse('view_batch')
        self.update_batch_url = reverse('update_batch')
        self.check_batch_id_url = reverse('check_batch_id')
        self.fetch_batch_data_url = reverse('fetch_batch_data')

        self.batch_data = {
            'batch_id': 'Batch001',
            'farm_name': 'Test Farm',
            'origin_country': 'Testland',
            'harvest_date': '2023-01-01',
            'processing_details': '',
            'roasting_date': '',
            'packaging_details': '',
            'packaging_date': '',
            'is_shipped': False,
            'is_delivered': False,
            'current_location': 'Test Location'
        }

        self.add_batch_data = {
            'batch_id': 'Batch001',
            'farm_name': 'Test Farm',
            'origin_country': 'Testland',
            'harvest_date': '2023-01-01'
        }

    @patch('blockchain.views.send_transaction')
    def test_add_batch_POST_new_batch(self, mock_send_transaction):
        mock_send_transaction.return_value = MockTransactionHash()
        response = self.client.post(self.add_batch_url, self.batch_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('0x123', response.content.decode())

    def test_add_batch_POST_existing_batch(self):
        Batch.objects.create(batch_id=self.batch_data['batch_id'])
        response = self.client.post(self.add_batch_url, self.batch_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Not available', response.content.decode())
