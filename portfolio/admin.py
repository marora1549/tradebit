from django.contrib import admin
from portfolio.models import Holding, HoldingClass


@admin.register(Holding)
class HoldingAdmin(admin.ModelAdmin):
    list_display = ('user', 'stock', 'quantity', 'avg_price', 'purchase_date')
    list_filter = ('user', 'purchase_date')
    search_fields = ('stock__symbol', 'stock__name', 'user__username', 'user__email')
    date_hierarchy = 'purchase_date'


@admin.register(HoldingClass)
class HoldingClassAdmin(admin.ModelAdmin):
    list_display = ('holding', 'classification')
    list_filter = ('classification',)
    search_fields = (
        'holding__stock__symbol', 
        'holding__stock__name', 
        'classification__name',
        'holding__user__username',
        'holding__user__email'
    )
