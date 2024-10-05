from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import CartItem
from products.models import Product
from django.contrib.auth.models import User
from decimal import Decimal

class CartTests(TestCase):
    
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
    def test_add_to_cart(self):
        data = {'product': self.product.id, 'quantity': 2}
        response = self.client.post(reverse('cart-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.get().quantity, 2)

    def test_view_cart(self):
        CartItem.objects.create(user=self.user, product=self.product, quantity=2)
        response = self.client.get(reverse('cart-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_update_cart_item_quantity(self):
        cart_item = CartItem.objects.create(user=self.user, product=self.product, quantity=2)
        data = {'quantity': 3}
        response = self.client.patch(reverse('cart-detail', kwargs={'pk': cart_item.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.get(id=cart_item.id).quantity, 3)

    def test_remove_from_cart(self):
        cart_item = CartItem.objects.create(user=self.user, product=self.product, quantity=2)
        response = self.client.delete(reverse('cart-detail', kwargs={'pk': cart_item.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_cart_total_price(self):
        CartItem.objects.create(user=self.user, product=self.product, quantity=2)
        response = self.client.get(reverse('cart-total-price'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_price'], Decimal('19.98'))
