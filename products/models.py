from django.db import models

from brands import models as brand_models
from campaigns.models import Campaign
# import analytics.models as analytics_models
from campaigns.constants import CATEGORY_CHOICES
from .constants import (
    CODE_POSITION_CHOICES
)


class Activity(models.Model):
    id = models.SmallAutoField(primary_key=True, db_column="activity_id")
    experience_type = models.CharField(max_length=200)

    class Meta:
        verbose_name = "activity"
        verbose_name_plural = "activities"

    def save(self, *args, **kwargs):
        if self.experience_type:
            self.experience_type = self.experience_type.replace(' ', '')
            for char in self.experience_type:
                if not char.isalnum():
                    self.experience_type = self.experience_type.replace(char, '')
        super(Activity, self).save(*args, **kwargs)

    def __str__(self):
        return self.experience_type


class Market(models.Model):
    market_name = models.CharField(max_length=150, primary_key=True)
    market_iso_code = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.market_name


class Product(models.Model):
    product_name = models.CharField(max_length=500)
    brand = models.ForeignKey(brand_models.Brand, on_delete=models.CASCADE, db_column="brand_code")
    campaign_name = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    product_description = models.CharField(max_length=400, blank=True, null=True)
    evrythng_tag_1 = models.CharField(max_length=200)
    evrythng_tag_2 = models.CharField(max_length=200, null=True, blank=True)
    evrythng_tag_3 = models.CharField(max_length=200, null=True, blank=True)
    evrythng_tag_4 = models.CharField(max_length=200, null=True, blank=True)
    code_position = models.CharField(max_length=100, choices=CODE_POSITION_CHOICES)
    requested_by = models.CharField(max_length=200)
    requested_date = models.DateField(auto_now_add=True)
    requester_email = models.EmailField()
    short_id = models.CharField(max_length=100, blank=True, null=True)
    gs1_link = models.URLField(blank=True, null=True)
    short_id_link = models.URLField(blank=True, null=True)
    # qr_code_img = models.FileField(upload_to='products_qr_codes/', blank=True, null=True)
    qr_code_img_url = models.URLField(blank=True, null=True)
    customized_qr_code_img_blob_url = models.URLField(blank=True, null=True)
    # market = models.ForeignKey(Market, on_delete=models.SET_NULL, null=True, db_column="market_name")
    # redirect_url = models.URLField()
    # launch_volume = models.BigIntegerField()
    # launch_date = models.DateField()
    # activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    # utm_tagged_link = models.CharField(max_length=200)

    class Meta:
        unique_together = (("product_name", "brand"),)

    def __str__(self) -> str:
        return self.product_name


class ProductMarketDetails(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE, db_column="market_name")
    is_default_market = models.BooleanField(default=False)
    redirect_url = models.URLField()
    estimated_annual_units = models.CharField(max_length=100)
    expected_launch_date = models.DateField()
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    utm_campaign = models.CharField(max_length=200)
    utm_content = models.CharField(max_length=200)
    utm_tagged_link = models.URLField()
    # brand = models.ForeignKey(Brand, on_delete=models.CASCADE, db_column="brand_code")
    # evrythng_tag_1 = models.CharField(max_length=200)
    # evrythng_tag_2 = models.CharField(max_length=200, null=True, blank=True)
    # evrythng_tag_3 = models.CharField(max_length=200, null=True, blank=True)
    # evrythng_tag_4 = models.CharField(max_length=200, null=True, blank=True)
    # code_placement = models.CharField(max_length=100, choices=CODE_PLACEMENT_CHOICES)
    # requested_by = models.CharField(max_length=200)
    # requested_date = models.DateField(auto_now_add=True)
    # budget_holder = models.EmailField()
    # gs1_link = models.URLField(blank=True, null=True)
    # utm_campaign = models.CharField(max_length=200)
    # utm_content = models.CharField(max_length=200)

    class Meta:
        verbose_name = "product market detail"
        verbose_name_plural = "product market details"
        unique_together = (("product", "market"),)

    def __str__(self) -> str:
        return f'{self.product.product_name} - {self.market.market_name}'


class SalesData(models.Model):
    product = models.ForeignKey(ProductMarketDetails, on_delete=models.CASCADE, db_column='product_name')
    market = models.ForeignKey(Market, on_delete=models.CASCADE, db_column="market_name")
    actual_unit_sales = models.PositiveBigIntegerField(blank=True, null=True)
    estimated_unit_sales = models.PositiveBigIntegerField(blank=True, null=True)
    from_date = models.DateField()
    to_date = models.DateField()

    class Meta:
        verbose_name = 'sales data'
        verbose_name_plural = 'sales data'

    def __str__(self) -> str:
        return f'{self.product.product.product_name} - {self.from_date} : {self.to_date}'


class PlanningDashboardDetails(models.Model):
    forecast_attributed_incremental_sales_volume = models.IntegerField()
    purchase_price = models.IntegerField()
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    local_brands = models.ForeignKey(brand_models.LocalBrand, on_delete=models.CASCADE)
    brand = models.ForeignKey(brand_models.Brand, on_delete=models.CASCADE)
    division = models.ForeignKey(brand_models.Division, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    products_category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    product_salesdata = models.ForeignKey(SalesData, on_delete=models.SET_NULL, null=True, blank=True)
    product_market_details = models.ForeignKey(ProductMarketDetails, on_delete=models.CASCADE)
    # google_analytics = models.ForeignKey(analytics_models.GoogleAnalytics, on_delete=models.SET_NULL, null=True, blank=True)
    cookie = models.CharField(max_length=150)
    data = models.CharField(max_length=500)
    dev_scans_data_4 = models.CharField(max_length=500)

    class Meta:
        verbose_name = "Planning Dashboard Details"
        verbose_name_plural = "Planning Dashboard Details"

    def __str__(self):
        return f'{self.brand}-{self.product}'


class QRCodeCutomizationTemplates(models.Model):
    template_name = models.CharField(max_length=100, default='QR Code Sample Template')
    qr_code_color = models.CharField(max_length=10)
    qr_code_logo_image = models.CharField(max_length=100, null=True, blank=True)
    qr_code_eye_shape = models.CharField(max_length=100)
    qr_code_background_color = models.CharField(max_length=10, default='#000000')
    sample_qr_code = models.FileField(upload_to='products_qr_codes', null=True, blank=True)
    sample_qr_code_blob_url = models.URLField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "QR Code Cutomization Templates"
        verbose_name_plural = "QR Code Cutomization Templates"

    def __str__(self):
        return self.template_name
