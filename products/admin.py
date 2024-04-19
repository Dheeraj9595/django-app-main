from django.contrib import admin

from .models import (
    Market,
    Product,
    Activity,
    SalesData,
    ProductMarketDetails,
    PlanningDashboardDetails,
    QRCodeCutomizationTemplates
)


class SalesDataAdmin(admin.ModelAdmin):
    list_display = ('product', 'market', 'from_date', 'to_date')
    search_fields = ('product__product_name', 'product__product_description', 'market__market_name', 'from_date', 'to_date')


admin.site.register(Activity)
admin.site.register(Product)
admin.site.register(ProductMarketDetails)
admin.site.register(Market)
admin.site.register(SalesData, SalesDataAdmin)
# admin.site.register(PlanningDashboardDetails)
admin.site.register(QRCodeCutomizationTemplates)
