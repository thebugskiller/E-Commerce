from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from products.models import Product
from cart.models import CartItem
from django.contrib.auth.models import User
from unittest.mock import patch
import stripe
from decimal import Decimal

class PaymentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(
            title='Test Product',
            price=9.99,
            description='Test description',
            category='Test Category',
            image='http://test.com/image.jpg'
        )
        CartItem.objects.create(user=self.user, product=self.product, quantity=2)

    @patch('stripe.Charge.create')
    def test_create_charge(self, mock_charge_create):
        mock_charge_create.return_value = {'id': 'ch_test123'}
        data = {'token': 'tok_visa'}
        response = self.client.post(reverse('create-charge'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], Decimal('19.98'))  # 9.99 * 2
        self.assertEqual(response.data['charge_id'], 'ch_test123')

    def test_create_charge_no_token(self):
        response = self.client.post(reverse('create-charge'), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('stripe.Charge.create')
    def test_create_charge_stripe_error(self, mock_charge_create):
        mock_charge_create.side_effect = ValueError("Invalid card token")
        data = {'token': 'invalid_token'}
        response = self.client.post(reverse('create-charge'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)