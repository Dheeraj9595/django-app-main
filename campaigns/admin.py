from django.contrib import admin

from .models import(
    Campaign,
    CampaignAdditionalDetails
)


class CampaignAdmin(admin.ModelAdmin):
    search_fields = ('campaign_name',)


class CampaignAdditionalDetailsAdmin(admin.ModelAdmin):
    search_fields = ('campaign__campaign_name',)


admin.site.register(Campaign, CampaignAdmin)
admin.site.register(CampaignAdditionalDetails, CampaignAdditionalDetailsAdmin)
