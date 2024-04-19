from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from backend.mixins import AdminLoginRequiredMixin

from .forms import CampaignForm
import brands.models as brand_models
from .constants import CATEGORY_CHOICES
from products import models as product_models
from products.constants import CODE_POSITION_CHOICES
from analytics.constants import (
    CODE_TYPE_CHOICES,
    CODE_PLACEMENT_CHOICES,
)


class CampaignFormView(AdminLoginRequiredMixin, View):
    """
        Campaign Form Views
    """
    def get(self, request):
        divisions = brand_models.Division.objects.filter(brand=None)
        local_brands = brand_models.LocalBrand.objects.all().exclude(brand=None)
        activities = product_models.Activity.objects.all()
        code_placement_choices = [
            {
                'value': choice[1],
                'acronym': choice[0]
            }
            for choice in CODE_POSITION_CHOICES
        ]
        utm_source_choices = [choice[0] for choice in CODE_PLACEMENT_CHOICES]
        utm_medium_choices = [choice[0] for choice in CODE_TYPE_CHOICES]
        category_choices = [choice[0] for choice in CATEGORY_CHOICES]
        markets = product_models.Market.objects.all()
        product_objs = product_models.Product.objects.all()
        return render(request, 'campaign_form.html', {"divisions": divisions, "local_brands": local_brands, "activities": activities, "product_objs": product_objs, "code_placement_choices": code_placement_choices, "utm_source_choices": utm_source_choices, "utm_medium_choices": utm_medium_choices, "category_choices": category_choices, "markets": markets})
        
    def post(self, request):
        success = False
        error_message = None
        data = request.POST
        form = CampaignForm(data)
        if form.is_valid():
            success, error_message, campaign_obj, campaign_detail_obj = form.save()
        else:
            error_message = form.errors.as_json()
            print(error_message)
        
        if success:
            campaign_obj.updated_by = request.user.username
            campaign_obj.save()
            messages.success(request, 'Campaign form submitted successfully.')
            qr_request_form_url = reverse('qr_request_form') + f"?campaign_id={campaign_obj.id}&market={data.get('market')}&launch_date={data.get('planned_launch_date')}"
            return redirect(qr_request_form_url)
        else:
            messages.error(request, f'Failed to submit Campaign form - {error_message}')
            return redirect('/custom_admin_dashboard')
