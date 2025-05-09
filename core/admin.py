from django.contrib import admin
from core.models import Stock, StockAlias, Classification


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'sector', 'industry')
    search_fields = ('symbol', 'name')
    list_filter = ('sector', 'industry')


@admin.register(StockAlias)
class StockAliasAdmin(admin.ModelAdmin):
    list_display = ('alias', 'stock')
    search_fields = ('alias', 'stock__symbol', 'stock__name')


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description')
    search_fields = ('name', 'type')
    list_filter = ('type',)
