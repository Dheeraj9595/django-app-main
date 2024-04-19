from django.urls import path

from .views import CampaignFormView


urlpatterns = [
    path('campaign_form/', CampaignFormView.as_view(), name="campaign_form"),
]