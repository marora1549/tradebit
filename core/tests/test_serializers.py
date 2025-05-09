from django.test import TestCase
from core.models import Stock, StockAlias, Classification
from core.serializers import StockSerializer, StockAliasSerializer, ClassificationSerializer


class StockSerializerTest(TestCase):
    """
    Test suite for the StockSerializer.
    """
    def setUp(self):
        self.stock_data = {
            'symbol': 'TCS',
            'name': 'Tata Consultancy Services',
            'sector': 'Technology',
            'industry': 'IT Services'
        }
        self.stock = Stock.objects.create(**self.stock_data)
        self.serializer = StockSerializer(instance=self.stock)

    def test_stock_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'symbol', 'name', 'sector', 'industry', 'is_active']))

    def test_stock_serializer_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['symbol'], self.stock_data['symbol'])
        self.assertEqual(data['name'], self.stock_data['name'])
        self.assertEqual(data['sector'], self.stock_data['sector'])
        self.assertEqual(data['industry'], self.stock_data['industry'])
        self.assertTrue(data['is_active'])


class StockAliasSerializerTest(TestCase):
    """
    Test suite for the StockAliasSerializer.
    """
    def setUp(self):
        self.stock = Stock.objects.create(
            symbol='HDFCBANK',
            name='HDFC Bank Ltd.',
            sector='Financial Services',
            industry='Banking'
        )
        self.alias = StockAlias.objects.create(
            stock=self.stock,
            alias='HDFC Bank'
        )
        self.serializer = StockAliasSerializer(instance=self.alias)

    def test_stock_alias_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'stock', 'alias', 'stock_details']))

    def test_stock_alias_serializer_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['alias'], 'HDFC Bank')
        self.assertEqual(data['stock'], self.stock.id)

    def test_stock_details_included(self):
        data = self.serializer.data
        self.assertEqual(data['stock_details']['symbol'], 'HDFCBANK')
        self.assertEqual(data['stock_details']['name'], 'HDFC Bank Ltd.')


class ClassificationSerializerTest(TestCase):
    """
    Test suite for the ClassificationSerializer.
    """
    def setUp(self):
        self.classification_data = {
            'name': 'Dividend Growth',
            'type': 'Strategy',
            'description': 'Companies with history of increasing dividends'
        }
        self.classification = Classification.objects.create(**self.classification_data)
        self.serializer = ClassificationSerializer(instance=self.classification)

    def test_classification_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'name', 'type', 'description']))

    def test_classification_serializer_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.classification_data['name'])
        self.assertEqual(data['type'], self.classification_data['type'])
        self.assertEqual(data['description'], self.classification_data['description'])
