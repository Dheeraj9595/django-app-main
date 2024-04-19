from django import forms
from datetime import datetime

from .models import(
    Campaign,
    CampaignAdditionalDetails
)
from brands import models as brand_models
from products import models as product_models
from analytics import models as analytics_models


class CampaignForm(forms.Form):
    """
        Campaign Form
    """
    TOGGLE_CHOICES = [
        ('on', True),
        ('off', False)
    ]
    key_contact_first_name = forms.CharField()
    key_contact_last_name = forms.CharField()
    key_contact_email_address = forms.EmailField()
    secondary_contact_first_name = forms.CharField(required=False)
    secondary_contact_last_name = forms.CharField(required=False)
    secondary_contact_email_address = forms.EmailField(required=False)
    division = forms.CharField()
    # local_brand = forms.CharField()
    # brand_code = forms.CharField()
    # global_brand_name = forms.CharField(required=False)
    # product_name = forms.CharField()
    # upc_ean_gtin = forms.CharField(required=False, max_length=14)
    category = forms.CharField()
    market = forms.CharField()
    activity_type = forms.CharField()
    # landing_page_url = forms.URLField()
    is_landing_page_on_an_external_third_party_site = forms.ChoiceField(choices=TOGGLE_CHOICES, required=False)
    does_landing_page_include_1pd_capture_or_signup = forms.ChoiceField(choices=TOGGLE_CHOICES, required=False)
    does_landing_page_include_option_to_purchase = forms.ChoiceField(choices=TOGGLE_CHOICES, required=False)
    if_yes_is_there_an_incentive_to_purchase = forms.ChoiceField(choices=TOGGLE_CHOICES, required=False)
    # estimated_total_or_annual_unit_volume = forms.IntegerField()
    planned_launch_date = forms.DateField()
    # utm_source = forms.CharField()
    # code_placement = forms.CharField()
    # utm_medium = forms.CharField()
    # utm_campaign = forms.CharField()
    # utm_term = forms.CharField()
    # utm_content = forms.CharField()
    # final_tagged_landing_page_url = forms.URLField()
    # ga_profile_id = forms.CharField(required=False)
    # asset_image_with_qr_code = forms.FileField()
    # code_url = forms.URLField()

    def save(self):
        success = True
        error_message = None
        campaign_obj=None
        campaign_detail_obj=None
        toggle_dict = {
            'on': True,
            'off': False
        }
        try:
            # print(self.data)
            # existing_campaign_detail_obj = CampaignAdditionalDetails.objects.first()
            campaign_obj = Campaign.objects.create(
                campaign_name=self.data.get('campaign_name').strip(),
                key_contact_first_name=self.data.get('key_contact_first_name').strip(),
                key_contact_last_name=self.data.get('key_contact_last_name').strip(),
                key_contact_email_address=self.data.get('key_contact_email_address').strip(),
                secondary_contact_first_name=self.data.get('secondary_contact_first_name').strip() if self.data.get('secondary_contact_first_name') else None,
                secondary_contact_last_name=self.data.get('secondary_contact_last_name').strip() if self.data.get('secondary_contact_last_name') else None,
                secondary_contact_email_address=self.data.get('secondary_contact_email_address').strip() if self.data.get('secondary_contact_email_address') else None,
                date_added=datetime.now(),
                date_updated=datetime.now()
            )
            divisions = self.data.getlist('division')
            # local_brands = self.data.getlist('local_brand')
            # brand_codes = self.data.getlist('brand_code')
            # global_brand_names = self.data.getlist('global_brand_name')
            # product_ids = self.data.getlist('product_name')
            # upc_ean_gtin_numbers = self.data.getlist('upc_ean_gtin')
            categories = self.data.getlist('category')
            market_ids = self.data.getlist('market')
            activities = self.data.getlist('activity_type')
            activity_type_names = self.data.getlist('activity_type_name')
            is_landing_page_on_an_external_third_party_site_inputs = self.data.getlist('is_landing_page_on_an_external_third_party_site')
            does_landing_page_include_1pd_capture_or_signup_inputs = self.data.getlist('does_landing_page_include_1pd_capture_or_signup')
            does_landing_page_include_option_to_purchase_inputs = self.data.getlist('does_landing_page_include_option_to_purchase')
            if_yes_is_there_an_incentive_to_purchase_inputs = self.data.getlist('if_yes_is_there_an_incentive_to_purchase')
            planned_launch_dates = self.data.getlist('planned_launch_date')
            for i in range(len(divisions)):
                division = brand_models.Division.objects.get(id=divisions[i])
                # local_brand = brand_models.LocalBrand.objects.get(id=local_brands[i])
                # brand = brand_models.Brand.objects.get(brand_code=brand_codes[i])
                # product = product_models.Product.objects.get(id=product_ids[i])
                # product_market_detail = product_models.ProductMarketDetails.objects.first()
                # print(product_market_detail)
                # analytics_obj = analytics_models.GoogleAnalytics.objects.first()
                market_obj = product_models.Market.objects.get(market_name=market_ids[i])
                if activities[i] == 'Other':
                    activity = product_models.Activity.objects.filter(experience_type=activity_type_names[i])
                    if not activity.exists():
                        activity = product_models.Activity.objects.create(
                            experience_type=activity_type_names[i]
                        )
                    else:
                        activity = activity.first()
                else:
                    activity = product_models.Activity.objects.get(id=activities[i])
                
                # activity = product_models.Activity.objects.get(id=activities[i])
                # if bool(len(is_landing_page_on_an_external_third_party_site_inputs)):
                #     is_landing_page_on_an_external_third_party_site_input=toggle_dict.get(is_landing_page_on_an_external_third_party_site_inputs.pop(i), False)
                # else:
                #     is_landing_page_on_an_external_third_party_site_input = False

                # if bool(len(does_landing_page_include_1pd_capture_or_signup_inputs)):
                #     does_landing_page_include_1pd_capture_or_signup_input=toggle_dict.get(does_landing_page_include_1pd_capture_or_signup_inputs.pop(i), False)
                # else:
                #     does_landing_page_include_1pd_capture_or_signup_input = False

                # if bool(len(does_landing_page_include_option_to_purchase_inputs)):
                #     does_landing_page_include_option_to_purchase_input=toggle_dict.get(does_landing_page_include_option_to_purchase_inputs.pop(i), False)
                # else:
                #     does_landing_page_include_option_to_purchase_input = False

                # if bool(len(if_yes_is_there_an_incentive_to_purchase_inputs)):
                #     if_yes_is_there_an_incentive_to_purchase_input=toggle_dict.get(if_yes_is_there_an_incentive_to_purchase_inputs.pop(i), False)
                # else:
                #     if_yes_is_there_an_incentive_to_purchase_input = False
                
                campaign_detail_obj = CampaignAdditionalDetails.objects.create(
                    campaign=campaign_obj,
                    division=division,
                    category=categories[i],
                    # market=market_obj,
                    # activity=activity,
                    # is_landing_page_on_an_external_third_party_site=is_landing_page_on_an_external_third_party_site_input,
                    # does_landing_page_include_1pd_capture_or_signup=does_landing_page_include_1pd_capture_or_signup_input,
                    # does_landing_page_include_option_to_purchase=does_landing_page_include_option_to_purchase_input,
                    # if_yes_is_there_an_incentive_to_purchase=if_yes_is_there_an_incentive_to_purchase_input,
                    planned_launch_date=datetime.strptime(self.data.get('planned_launch_date'), "%Y-%m-%d").date()
                )

        except Exception as error:
            success = False
            error_message = str(error)
            print(error)

        finally:
            return success, error_message, campaign_obj, campaign_detail_obj
