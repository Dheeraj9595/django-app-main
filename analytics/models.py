from django.db import models

from brands.models import Brand
from products.models import Product
from campaigns.models import Campaign
from .constants import (
    CODE_TYPE_CHOICES,
    CODE_PLACEMENT_CHOICES
)


class GoogleAnalytics(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column="product_name")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, db_column="brand_code")
    code_placement = models.CharField(max_length=100, choices=CODE_PLACEMENT_CHOICES)
    code_type = models.CharField(max_length=13, choices=CODE_TYPE_CHOICES)
    # utm_campaign = models.CharField(max_length=200)
    variant = models.CharField(max_length=200, blank=True, null=True)
    # utm_content = models.CharField(max_length=200)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, db_column="campaign_name", null=True)

    class Meta:
        verbose_name = "google analytics"
        verbose_name_plural = "google analytics"

    def __str__(self) -> str:
        return f'{self.brand.brand_code}-{self.product.product_name}'
