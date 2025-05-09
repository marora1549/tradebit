from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """
    An abstract base model that provides self-updating
    created and modified timestamps.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Stock(TimeStampedModel):
    """
    Model representing a stock in the market.
    """
    symbol = models.CharField(_('Symbol'), max_length=20, unique=True)
    name = models.CharField(_('Company Name'), max_length=100)
    sector = models.CharField(_('Sector'), max_length=100, blank=True, null=True)
    industry = models.CharField(_('Industry'), max_length=100, blank=True, null=True)
    is_active = models.BooleanField(_('Is Active'), default=True)

    class Meta:
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')
        ordering = ['symbol']

    def __str__(self):
        return f"{self.symbol} - {self.name}"


class StockAlias(TimeStampedModel):
    """
    Model representing alternative names/symbols for a stock.
    This is useful for mapping common names to NSE symbols.
    """
    stock = models.ForeignKey(
        Stock, 
        on_delete=models.CASCADE, 
        related_name='aliases',
        verbose_name=_('Stock')
    )
    alias = models.CharField(_('Alias'), max_length=50)

    class Meta:
        verbose_name = _('Stock Alias')
        verbose_name_plural = _('Stock Aliases')
        unique_together = ['stock', 'alias']

    def __str__(self):
        return f"{self.alias} -> {self.stock.symbol}"


class Classification(TimeStampedModel):
    """
    Model representing a custom classification for holdings.
    Examples: "Dividend Stocks", "Long Term", "Sector: Technology".
    """
    name = models.CharField(_('Name'), max_length=100)
    type = models.CharField(_('Type'), max_length=50)
    description = models.TextField(_('Description'), blank=True, null=True)

    class Meta:
        verbose_name = _('Classification')
        verbose_name_plural = _('Classifications')
        unique_together = ['name', 'type']
        ordering = ['type', 'name']

    def __str__(self):
        return f"{self.type}: {self.name}"
