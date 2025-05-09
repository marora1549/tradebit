from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Stock, Classification
from portfolio.models import Holding, HoldingClass
from portfolio.serializers import HoldingSerializer, HoldingClassSerializer

User = get_user_model()


class HoldingSerializerTest(TestCase):
    """
    Test suite for the HoldingSerializer.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.stock = Stock.objects.create(
            symbol='INFY',
            name='Infosys Ltd.',
            sector='Technology',
            industry='IT Services'
        )
        self.holding = Holding.objects.create(
            user=self.user,
            stock=self.stock,
            quantity=Decimal('15.0000'),
            avg_price=Decimal('1200.00'),
            purchase_date='2023-03-10'
        )
        self.serializer = HoldingSerializer(instance=self.holding)

    def test_holding_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set([
                'id', 'user', 'stock', 'quantity', 'avg_price',
                'purchase_date', 'notes', 'source', 'external_id',
                'stock_details', 'user_details', 'total_value',
                'created_at', 'updated_at'
            ])
        )

    def test_holding_serializer_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['user'], self.user.id)
        self.assertEqual(data['stock'], self.stock.id)
        self.assertEqual(Decimal(data['quantity']), Decimal('15.0000'))
        self.assertEqual(Decimal(data['avg_price']), Decimal('1200.00'))
        self.assertEqual(data['purchase_date'], '2023-03-10')
        self.assertEqual(Decimal(data['total_value']), Decimal('18000.00'))

    def test_stock_details_included(self):
        data = self.serializer.data
        self.assertEqual(data['stock_details']['symbol'], 'INFY')
        self.assertEqual(data['stock_details']['name'], 'Infosys Ltd.')


class HoldingClassSerializerTest(TestCase):
    """
    Test suite for the HoldingClassSerializer.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.stock = Stock.objects.create(
            symbol='TCS',
            name='Tata Consultancy Services',
            sector='Technology',
            industry='IT Services'
        )
        self.holding = Holding.objects.create(
            user=self.user,
            stock=self.stock,
            quantity=Decimal('8.0000'),
            avg_price=Decimal('3200.00'),
            purchase_date='2023-04-05'
        )
        self.classification = Classification.objects.create(
            name='Dividend Payer',
            type='Income',
            description='Companies that consistently pay dividends'
        )
        self.holding_class = HoldingClass.objects.create(
            holding=self.holding,
            classification=self.classification
        )
        self.serializer = HoldingClassSerializer(instance=self.holding_class)

    def test_holding_class_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set([
                'id', 'holding', 'classification',
                'holding_details', 'classification_details',
                'created_at', 'updated_at'
            ])
        )

    def test_holding_class_serializer_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['holding'], self.holding.id)
        self.assertEqual(data['classification'], self.classification.id)

    def test_related_details_included(self):
        data = self.serializer.data
        self.assertEqual(
            data['holding_details']['stock_details']['symbol'], 
            'TCS'
        )
        self.assertEqual(
            data['classification_details']['name'],
            'Dividend Payer'
        )
