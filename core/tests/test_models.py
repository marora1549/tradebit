from django.test import TestCase
from core.models import Stock, StockAlias, Classification


class StockModelTest(TestCase):
    """
    Test suite for the Stock model.
    """
    def setUp(self):
        self.stock = Stock.objects.create(
            symbol="RELIANCE",
            name="Reliance Industries Ltd.",
            sector="Energy",
            industry="Oil & Gas"
        )

    def test_stock_creation(self):
        self.assertEqual(self.stock.symbol, "RELIANCE")
        self.assertEqual(self.stock.name, "Reliance Industries Ltd.")
        self.assertEqual(self.stock.sector, "Energy")
        self.assertEqual(self.stock.industry, "Oil & Gas")
        self.assertTrue(self.stock.is_active)

    def test_stock_str_representation(self):
        self.assertEqual(str(self.stock), "RELIANCE - Reliance Industries Ltd.")


class StockAliasModelTest(TestCase):
    """
    Test suite for the StockAlias model.
    """
    def setUp(self):
        self.stock = Stock.objects.create(
            symbol="INFY",
            name="Infosys Ltd.",
            sector="Technology",
            industry="IT Services"
        )
        self.alias = StockAlias.objects.create(
            stock=self.stock,
            alias="Infosys"
        )

    def test_stock_alias_creation(self):
        self.assertEqual(self.alias.stock, self.stock)
        self.assertEqual(self.alias.alias, "Infosys")

    def test_stock_alias_str_representation(self):
        self.assertEqual(str(self.alias), "Infosys -> INFY")


class ClassificationModelTest(TestCase):
    """
    Test suite for the Classification model.
    """
    def setUp(self):
        self.classification = Classification.objects.create(
            name="Long Term",
            type="Investment Horizon",
            description="Investments intended to be held for 3+ years"
        )

    def test_classification_creation(self):
        self.assertEqual(self.classification.name, "Long Term")
        self.assertEqual(self.classification.type, "Investment Horizon")
        self.assertEqual(
            self.classification.description, 
            "Investments intended to be held for 3+ years"
        )

    def test_classification_str_representation(self):
        self.assertEqual(str(self.classification), "Investment Horizon: Long Term")
