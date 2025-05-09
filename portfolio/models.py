from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel, Stock, Classification


class Holding(TimeStampedModel):
    """
    Model representing a stock holding in a user's portfolio.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='holdings',
        verbose_name=_('User')
    )
    stock = models.ForeignKey(
        'core.Stock',
        on_delete=models.CASCADE,
        related_name='holdings',
        verbose_name=_('Stock')
    )
    quantity = models.DecimalField(
        _('Quantity'),
        max_digits=15,
        decimal_places=4
    )
    avg_price = models.DecimalField(
        _('Average Price'),
        max_digits=15,
        decimal_places=2
    )
    purchase_date = models.DateField(
        _('Purchase Date')
    )
    notes = models.TextField(
        _('Notes'),
        blank=True,
        null=True
    )
    source = models.CharField(
        _('Source'),
        max_length=50,
        blank=True,
        null=True,
        help_text=_('Source of the holding data (e.g., manual, zerodha, upstox)')
    )
    external_id = models.CharField(
        _('External ID'),
        max_length=100,
        blank=True,
        null=True,
        help_text=_('ID used by the external system if imported')
    )

    class Meta:
        verbose_name = _('Holding')
        verbose_name_plural = _('Holdings')
        unique_together = ['user', 'stock', 'purchase_date']
        ordering = ['-purchase_date']

    def __str__(self):
        return f"{self.user.username} - {self.stock.symbol} ({self.quantity})"

    @property
    def total_value(self):
        """
        Calculate the total value of the holding based on the purchase price.
        """
        return self.quantity * self.avg_price


class HoldingClass(TimeStampedModel):
    """
    Model representing a classification associated with a specific holding.
    """
    holding = models.ForeignKey(
        Holding,
        on_delete=models.CASCADE,
        related_name='classifications',
        verbose_name=_('Holding')
    )
    classification = models.ForeignKey(
        'core.Classification',
        on_delete=models.CASCADE,
        related_name='holdings',
        verbose_name=_('Classification')
    )

    class Meta:
        verbose_name = _('Holding Classification')
        verbose_name_plural = _('Holding Classifications')
        unique_together = ['holding', 'classification']

    def __str__(self):
        return f"{self.holding.stock.symbol} - {self.classification.name}"
