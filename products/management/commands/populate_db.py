import requests
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Populate database with products from fakestoreapi.com'

    def handle(self, *args, **kwargs):
        url = 'https://fakestoreapi.com/products'
        response = requests.get(url)
        products = response.json()

        for product_data in products:
            Product.objects.create(
                title=product_data['title'],
                price=product_data['price'],
                description=product_data['description'],
                category=product_data['category'],
                image=product_data['image']
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated database with {len(products)} products'))