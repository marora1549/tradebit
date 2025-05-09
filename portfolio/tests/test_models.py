from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Stock, Classification
from portfolio.models import Holding, HoldingClass

User = get_user_model()


class HoldingModelTest(TestCase):
    """
    Test suite for the Holding model.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.stock = Stock.objects.create(
            symbol='TATAMOTORS',
            name='Tata Motors Ltd.',
            sector='Automobile',
            industry='Auto - Cars/Utility Vehicles'
        )
        self.holding = Holding.objects.create(
            user=self.user,
            stock=self.stock,
            quantity=Decimal('10.0000'),
            avg_price=Decimal('500.00'),
            purchase_date='2023-01-15'
        )

    def test_holding_creation(self):
        self.assertEqual(self.holding.user, self.user)
        self.assertEqual(self.holding.stock, self.stock)
        self.assertEqual(self.holding.quantity, Decimal('10.0000'))
        self.assertEqual(self.holding.avg_price, Decimal('500.00'))
        self.assertEqual(str(self.holding.purchase_date), '2023-01-15')

    def test_holding_str_representation(self):
        self.assertEqual(
            str(self.holding),
            f"testuser - TATAMOTORS (10.0000)"
        )

    def test_total_value_calculation(self):
        self.assertEqual(self.holding.total_value, Decimal('5000.00'))


class HoldingClassModelTest(TestCase):
    """
    Test suite for the HoldingClass model.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.stock = Stock.objects.create(
            symbol='HDFCBANK',
            name='HDFC Bank Ltd.',
            sector='Financial Services',
            industry='Banking'
        )
        self.holding = Holding.objects.create(
            user=self.user,
            stock=self.stock,
            quantity=Decimal('5.0000'),
            avg_price=Decimal('1500.00'),
            purchase_date='2023-02-20'
        )
        self.classification = Classification.objects.create(
            name='Blue Chip',
            type='Quality',
            description='Well-established, financially sound companies'
        )
        self.holding_class = HoldingClass.objects.create(
            holding=self.holding,
            classification=self.classification
        )

    def test_holding_class_creation(self):
        self.assertEqual(self.holding_class.holding, self.holding)
        self.assertEqual(self.holding_class.classification, self.classification)

    def test_holding_class_str_representation(self):
        self.assertEqual(
            str(self.holding_class),
            "HDFCBANK - Blue Chip"
        )
