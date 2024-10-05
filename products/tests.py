from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product
from django.contrib.auth.models import User

class ProductTests(TestCase):
    
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

    def test_get_all_products(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_single_product(self):
        response = self.client.get(reverse('product-detail', kwargs={'pk': self.product.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Product')

    def test_sort_products_by_price_asc(self):
        Product.objects.create(title='Cheap Product', price=5.99, description='Cheap', category='Test', image='http://test.com/cheap.jpg')
        response = self.client.get(reverse('product-sort-by-price') + '?order=asc')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Cheap Product')

    def test_sort_products_by_price_desc(self):
        Product.objects.create(title='Expensive Product', price=15.99, description='Expensive', category='Test', image='http://test.com/expensive.jpg')
        response = self.client.get(reverse('product-sort-by-price') + '?order=desc')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Expensive Product')
