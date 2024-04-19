from django.db import models

from .constants import CATEGORY_CHOICES
from products.constants import CODE_POSITION_CHOICES
from analytics.constants import(
    CODE_TYPE_CHOICES,
    CODE_PLACEMENT_CHOICES
)
# from products.models import(
#     Market,
#     Activity
# )
from brands.models import(
    Brand,
    Division,
    LocalBrand
)


class Campaign(models.Model):
    campaign_name = models.CharField(max_length=500)
    key_contact_first_name = models.CharField(max_length=500)
    key_contact_last_name = models.CharField(max_length=500)
    key_contact_email_address = models.EmailField()
    secondary_contact_first_name = models.CharField(max_length=500, blank=True, null=True)
    secondary_contact_last_name = models.CharField(max_length=500, blank=True, null=True)
    secondary_contact_email_address = models.EmailField(blank=True, null=True)
    date_added = models.DateField(auto_now=True)
    date_updated = models.DateField(auto_now_add=True)
    updated_by = models.CharField(max_length=500, null=True)

    def __str__(self) -> str:
        return f'{self.pk} - {self.campaign_name}'


class CampaignAdditionalDetails(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    # local_brand_name = models.ForeignKey(LocalBrand, on_delete=models.CASCADE)
    # brand_code = models.ForeignKey(Brand, on_delete=models.CASCADE)
    # global_brand_name = models.CharField(max_length=500, blank=True, null=True)
    # product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    # upc_ean_gtin = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    # market = models.ForeignKey(Market, on_delete=models.CASCADE)
    # activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    # landing_page_url = models.URLField()
    is_landing_page_on_an_external_third_party_site = models.BooleanField(default=False)
    does_landing_page_include_1pd_capture_or_signup = models.BooleanField(default=False)
    does_landing_page_include_option_to_purchase = models.BooleanField(default=False)
    if_yes_is_there_an_incentive_to_purchase = models.BooleanField(default=False)
    # estimated_total_or_annual_unit_volume = models.IntegerField()
    planned_launch_date = models.DateField()
    # code_placement = models.CharField(max_length=100, choices=CODE_PLACEMENT_CHOICES)
    # code_position = models.CharField(max_length=100, choices=CODE_POSITION_CHOICES, null=True)
    # code_type = models.CharField(max_length=13, choices=CODE_TYPE_CHOICES, null=True)
    # utm_campaign = models.CharField(max_length=200)
    # variant = models.CharField(max_length=200)
    # utm_content = models.CharField(max_length=200)
    # final_tagged_landing_page_url = models.URLField()
    # ga_profile_id = models.CharField(max_length=500, blank=True, null=True)
    # asset_image_with_qr_code = models.FileField(upload_to='asset_images_with_qr_code/', blank=True, null=True)
    # code_url = models.URLField()

    class Meta:
        verbose_name = "campaign additional details"
        verbose_name_plural = "campaign additional details"

    def __str__(self) -> str:
        return f'{self.pk} - {self.campaign.campaign_name} campaign additional details'
