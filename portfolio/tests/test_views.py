from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from core.models import Stock, Classification
from portfolio.models import Holding, HoldingClass

User = get_user_model()


class HoldingViewSetTest(APITestCase):
    """
    Test suite for the HoldingViewSet API endpoints.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.stock = Stock.objects.create(
            symbol='RELIANCE',
            name='Reliance Industries Ltd.',
            sector='Energy',
            industry='Oil & Gas'
        )
        
        self.holding_data = {
            'user': self.user.id,
            'stock': self.stock.id,
            'quantity': '10.0000',
            'avg_price': '2000.00',
            'purchase_date': '2023-05-01'
        }
        
        self.holding = Holding.objects.create(**self.holding_data)

    def test_list_holdings(self):
        url = reverse('holding-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_holding(self):
        url = reverse('holding-detail', args=[self.holding.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stock'], self.stock.id)

    def test_create_holding(self):
        new_stock = Stock.objects.create(
            symbol='INFY',
            name='Infosys Ltd.',
            sector='Technology',
            industry='IT Services'
        )
        
        new_holding_data = {
            'user': self.user.id,
            'stock': new_stock.id,
            'quantity': '5.0000',
            'avg_price': '1500.00',
            'purchase_date': '2023-06-01'
        }
        
        url = reverse('holding-list')
        response = self.client.post(url, new_holding_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Holding.objects.count(), 2)

    def test_update_holding(self):
        url = reverse('holding-detail', args=[self.holding.id])
        updated_data = {
            'user': self.user.id,
            'stock': self.stock.id,
            'quantity': '15.0000',  # Updated quantity
            'avg_price': '2100.00',  # Updated price
            'purchase_date': '2023-05-01'
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.holding.refresh_from_db()
        self.assertEqual(self.holding.quantity, Decimal('15.0000'))
        self.assertEqual(self.holding.avg_price, Decimal('2100.00'))

    def test_delete_holding(self):
        url = reverse('holding-detail', args=[self.holding.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Holding.objects.count(), 0)


class HoldingClassViewSetTest(APITestCase):
    """
    Test suite for the HoldingClassViewSet API endpoints.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.stock = Stock.objects.create(
            symbol='HDFCBANK',
            name='HDFC Bank Ltd.',
            sector='Financial Services',
            industry='Banking'
        )
        
        self.holding = Holding.objects.create(
            user=self.user,
            stock=self.stock,
            quantity=Decimal('10.0000'),
            avg_price=Decimal('1600.00'),
            purchase_date='2023-07-01'
        )
        
        self.classification = Classification.objects.create(
            name='Blue Chip',
            type='Quality',
            description='Well-established, financially sound companies'
        )
        
        self.holding_class_data = {
            'holding': self.holding.id,
            'classification': self.classification.id
        }
        
        self.holding_class = HoldingClass.objects.create(**self.holding_class_data)

    def test_list_holding_classes(self):
        url = reverse('holdingclass-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_holding_class(self):
        url = reverse('holdingclass-detail', args=[self.holding_class.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['holding'], self.holding.id)
        self.assertEqual(response.data['classification'], self.classification.id)

    def test_create_holding_class(self):
        new_classification = Classification.objects.create(
            name='Dividend Payer',
            type='Income',
            description='Companies that consistently pay dividends'
        )
        
        new_holding_class_data = {
            'holding': self.holding.id,
            'classification': new_classification.id
        }
        
        url = reverse('holdingclass-list')
        response = self.client.post(url, new_holding_class_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HoldingClass.objects.count(), 2)

    def test_delete_holding_class(self):
        url = reverse('holdingclass-detail', args=[self.holding_class.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HoldingClass.objects.count(), 0)
