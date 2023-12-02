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

    @patch('blockchain.views.contract.functions.getBatchDetails')
    def test_view_batch_POST_valid_batch(self, mock_get_batch_details):
        mock_get_batch_details.return_value.call.return_value = (self.batch_data, True)
        Batch.objects.create(batch_id=self.batch_data['batch_id'])
        response = self.client.post(self.view_batch_url, {'batch_id': self.batch_data['batch_id']})
        self.assertEqual(response.status_code, 200)

    @patch('blockchain.views.send_transaction')
    def test_update_batch_POST(self, mock_send_transaction):
        # Use MockTransactionHash as the return value for the mocked function
        mock_send_transaction.return_value = MockTransactionHash()
        Batch.objects.create(batch_id=self.batch_data['batch_id'])

        updated_data = {**self.batch_data, 'new_processing_details': 'Updated Processing'}
        response = self.client.post(self.update_batch_url, updated_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('0x123', response.content.decode())

    def test_check_batch_id_POST(self):
        response = self.client.post(self.check_batch_id_url, {'batch_id': 'Batch002'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'available': True})

    @patch('blockchain.views.contract.functions.getBatchDetails')
    def test_fetch_batch_data_POST_valid_batch(self, mock_get_batch_details):
        mock_get_batch_details.return_value.call.return_value = (self.batch_data, True)
        Batch.objects.create(batch_id=self.batch_data['batch_id'])
        response = self.client.post(self.fetch_batch_data_url, {'batch_id': self.batch_data['batch_id']},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_fetch_batch_data_POST_invalid_batch(self):
        response = self.client.post(self.fetch_batch_data_url, {'batch_id': 'InvalidBatchID'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {'success': False, 'error': 'BatchID does not exist in the local database'})
