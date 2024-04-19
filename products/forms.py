import os
from django import forms
from datetime import datetime
from django.db.models import(
    Case,
    When,
    Value,
    IntegerField
)
from django.core.exceptions import ImproperlyConfigured

from backend.constants import(
    GS1_LINK_FORMAT,
    OR_CODE_LINK_FORMAT,
    SHORT_ID_LINK_FORMAT,
    GS1_OR_CODE_LINK_FORMAT
)
from brands import models as brand_models
import campaigns.models as campaign_models
from analytics import models as analytics_models
from products.constants import CODE_POSITION_CHOICES
from analytics.constants import(
    CODE_TYPE_CHOICES,
    CODE_PLACEMENT_CHOICES,
)
from backend.utils import (
    create_evrythng_project,
    create_evrythng_product,
    generate_evrythng_qr_code,
    create_evrythng_project_application,
    create_evrythng_product_redirection,
    create_evrythng_account_level_redirector,
    create_evrythng_application_level_redirector,
)
from .models import (
    Market,
    Product,
    SalesData,
    Activity,
    ProductMarketDetails,
    PlanningDashboardDetails
)
from brands import models as brand_models
from campaigns.constants import CATEGORY_CHOICES
from django.db.utils import ProgrammingError


class ORRequestForm(forms.Form):
    """
        QR Request Form
    """
    try:
        division_choices = [("", 'Select Division')] + [(division.id, division.division) for division in brand_models.Division.objects.filter(brand=None)]
        local_brand_choices = [("", 'Select Local Brand')] + [(local_brand.id, local_brand.local_brand_name) for local_brand in brand_models.LocalBrand.objects.all().exclude(brand=None)] + [('Other', 'Other')]
        campaign_choices = [("", 'Select Campaign')] + [(campaign.id, campaign.campaign_name) for campaign in campaign_models.Campaign.objects.all()]
        experience_type_choices = [("", 'Select Experience Type')] + [(activity.id, activity.experience_type) for activity in Activity.objects.all()] + [('Other', 'Other')]
        code_position_choices = [("", 'Select Code Position')] + [(choice[0], choice[1]) for choice in CODE_POSITION_CHOICES]
        code_placement_choices = [("", 'Select Code Placement')] + [(choice[0], choice[1]) for choice in CODE_PLACEMENT_CHOICES]
        code_type_choices = [("", 'Select Code Type')] + [(choice[0], choice[1]) for choice in CODE_TYPE_CHOICES]
        division = forms.ChoiceField(choices=division_choices, widget=forms.Select(attrs={"class": "form-select", "id": "division_input_1_1", "required": "required"}))
        local_brand = forms.ChoiceField(choices=local_brand_choices, widget=forms.Select(attrs={"class": "form-select", "id": "local_brand_input_1_1", "onClick": "hidden_fields_show(this);", "onChange": "add_brand_code(this)", "required": "required"}))
        local_brand_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "id": "local_brand_name_input_1_1"}))
        brand_code = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id": "brand_code_input_1_1", "onChange": "utm_campaign_value_add(this);", "required": "required", "readonly": "readonly"}))
        experience_type = forms.ChoiceField(choices=experience_type_choices, widget=forms.Select(attrs={"class": "form-select experience_type_input", "id": "experience_type_input_1_1", "onClick": "hidden_fields_show(this);", "onChange": "utm_content_value_add(this)", "required": "required"}))
        experience_type_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control experience_type_name_input", "id": "experience_type_name_input_1_1", "onChange": "utm_content_value_add(this)", "onInput": "this.value=this.value.split(' ')[0]"}))
        global_brand_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'global_brand_name_input_1_1'}))
        upc_ean_gtin = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "id": "upc_ean_gtin_input_1_1", "maxlength": 14, "onInput": "fix_maxlength(this);", "onChange": "upc_ean_gtin_prefix_add(this);"}))
        product_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id": "product_name_input_1_1", "onInput": "check_duplicate_products(this);", "required": "required"}))
        product_description = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control", "id": "product_description_input_1_1", "rows": "3"}))
        market = forms.ModelChoiceField(queryset=Market.objects.all(), widget=forms.Select(attrs={"class": "form-select market_input", "id": "market_input_1_1", "onChange": "add_iso_code(this);", "required": "required"}))
        market_iso_code = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control iso_input", "id": "iso_input_1_1", "onChange": "utm_campaign_value_add(this);", "readonly": "readonly", "required": "required"}))
        redirect_url = forms.URLField(widget=forms.URLInput(attrs={"class": "form-control redirect_url_input", "id": "redirect_url_input_1_1", "onChange": "correct_redirect_url(this);", "placeholder": "https://www.example.com", "required": "required"}))
        estimated_annual_units = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control estimated_annual_units_input", "id": "estimated_annual_units_input_1_1", "onInput": "add_comma_in_estimated_annual_units(this);", "required": "required"}))
        expected_launch_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control expected_launch_date_input", "id": "expected_launch_date_input_1_1", "required": "required"}))
        utm_tagged_link = forms.URLField(required=False, widget=forms.URLInput(attrs={"class": "form-control utm_tagged_link_input", "id": "utm_tagged_link_input_1_1", "readonly": "readonly", "required": "required"}))
        tag1 = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id": "tag1_input_1_1", "onKeyup": "remove_space_and_make_lower_case_value(this);", "onChange": "utm_campaign_value_add(this);", "readonly" : "readonly", "required": "required"}))
        tag2 = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "id": "tag2_input_1_1", "onKeyup": "remove_space_and_make_lower_case_value(this);"}))
        tag3 = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "id": "tag3_input_1_1", "onKeyup": "remove_space_and_make_lower_case_value(this);"}))
        tag4 = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "id": "tag4_input_1_1", "onKeyup": "remove_space_and_make_lower_case_value(this);"}))
        code_position = forms.ChoiceField(choices=code_position_choices, widget=forms.Select(attrs={"class": "form-select", "id": "code_position_input_1_1", "onChange": "utm_content_value_add(this)", "required": "required"}))
        requested_by = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id": "requested_by_input_1_1", "required": "required"}))
        date_requested = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control", "id": "date_requested_input_1_1", "required": "required"}))
        requester_email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "id": "requester_email_input_1_1", "placeholder": "me@me.com", "required": "required"}))
        campaign_name = forms.ChoiceField(choices=campaign_choices, widget=forms.Select(attrs={"class": "form-select", "id": "campaign_name_input_1_1", "onChange": "tag1_value_add(this);", "required": "required"}))
        code_placement = forms.ChoiceField(choices=code_placement_choices, widget=forms.Select(attrs={"class": "form-select", "id": "code_placement_input_1_1", "onChange": "utm_tagged_link_value_add();", "required": "required"}))
        code_type = forms.ChoiceField(choices=code_type_choices, widget=forms.Select(attrs={"class": "form-select", "id": "code_type_input_1_1", "onChange": "utm_tagged_link_value_add();", "required": "required"}))
        utm_campaign = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control utm_campaign_input", "id": "utm_campaign_input_1_1", "onChange": "utm_tagged_link_value_add();", "readonly": "readonly", "required": "required"}))
        variant = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "id": "variant_input_1_1", "onChange": "utm_tagged_link_value_add();", "onKeyup": "remove_space_and_make_lower_case_value(this);"}))
        utm_content = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control utm_content_input", "id": "utm_content_input_1_1", "onChange": "utm_tagged_link_value_add();", "readonly": "readonly", "required": "required"}))
    except ProgrammingError:
        print('-----------ProgrammingError in ORRequestForm run migrations or check the error cause-------------')
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['division'].choices = [("", 'Select Division')] + [(division.id, division.division) for division in brand_models.Division.objects.filter(brand=None)]
        self.fields['local_brand'].choices = [("", 'Select Local Brand')] + [(local_brand.id, local_brand.local_brand_name) for local_brand in brand_models.LocalBrand.objects.all().exclude(brand=None)] + [('Other', 'Other')]
        self.fields['experience_type'].choices = [("", 'Select Experience Type')] + [(activity.id, activity.experience_type) for activity in Activity.objects.all()] + [('Other', 'Other')]
        self.fields['code_position'].choices = [("", 'Select Code Position')] + [(choice[0], choice[1]) for choice in CODE_POSITION_CHOICES]
        self.fields['code_placement'].choices = [("", 'Select Code Placement')] + [(choice[0], choice[1]) for choice in CODE_PLACEMENT_CHOICES]
        self.fields['code_type'].choices = [("", 'Select Code Type')] + [(choice[0], choice[1]) for choice in CODE_TYPE_CHOICES]
        self.fields['campaign_name'].choices = [("", 'Select Campaign')] + [(campaign.id, campaign.campaign_name) for campaign in campaign_models.Campaign.objects.all()]

    def save(self):
        success = True
        error_message = None
        customize_qr_product = None
        try:
            division = brand_models.Division.objects.get(id=self.data.get('division')[0])
            campaign = campaign_models.Campaign.objects.get(id=self.data.get('campaign_name')[0])
            local_brand_name = self.data.get('local_brand_name')[0]
            if local_brand_name:
                local_brand_name = local_brand_name.strip()
                local_brand = brand_models.LocalBrand.objects.filter(local_brand_name=local_brand_name)
                if not local_brand.exists():
                    local_brand = brand_models.LocalBrand.objects.create(
                        local_brand_name=local_brand_name
                    )
                else:
                    local_brand = local_brand.first()
            else:
                local_brand = brand_models.LocalBrand.objects.get(id=self.data.get('local_brand')[0])
            
            brand_code = self.data.get('brand_code')[0]
            if brand_code:
                brand = brand_models.Brand.objects.filter(brand_code=brand_code.strip())
                if brand.exists():
                    brand = brand.first()
                    brand.division = division
                    brand.local_brand = local_brand
                    brand.global_brand_name = self.data.get('global_brand_name')[0].strip() if self.data.get('global_brand_name')[0] else None
                    brand.upc_ean_gtin = self.data.get('upc_ean_gtin')[0].strip() if self.data.get('upc_ean_gtin')[0] else None
                    brand.save()
                else:
                    brand = brand_models.Brand.objects.create(
                        brand_code=brand_code,
                        local_brand=local_brand,
                        division=division,
                        global_brand_name=self.data.get('global_brand_name')[0].strip() if self.data.get('global_brand_name')[0] else None,
                        upc_ean_gtin = self.data.get('upc_ean_gtin')[0].strip() if self.data.get('upc_ean_gtin')[0] else None
                    )
                
                gs1_link = None
                tags_list = ['tag1', 'tag2', 'tag3', 'tag4']
                tags = [self.data.get(tag)[0].strip() for tag in tags_list if self.data.get(tag)[0] is not None and bool(len(self.data.get(tag)[0]))]
                evrythng_short_domain = os.environ.get('EVRYTHNG_SHORT_DOMAIN')
                if brand.upc_ean_gtin and evrythng_short_domain:
                    gs1_link = GS1_LINK_FORMAT.format(evrythng_short_domain, brand.upc_ean_gtin)
                
                product_name = self.data.get('product_name')[0].strip()
                product_description = self.data.get('product_description')[0].strip()
                campaign_name = campaign.campaign_name
                product = Product.objects.filter(product_name=product_name)
                # project = project_models.Project.objects.filter(project_name=project_name)
                if not product.exists():
                    market_names = self.data.get('market')
                    market_objs = Market.objects.filter(
                        market_name__in=market_names
                    ).annotate(
                        country_order=Case(
                            *[When(market_name=country, then=Value(i)) for i, country in enumerate(market_names)],
                            output_field=IntegerField(),
                        )
                    ).order_by('country_order')
                    print(self.data.get('market'))
                    print(market_objs)
                    print(market_objs.count())
                    market_iso_codes = self.data.get('market_iso_code')
                    utm_tagged_links = self.data.get('utm_tagged_link')
                    redirect_urls = self.data.get('redirect_url')
                    estimated_annual_units = self.data.get('estimated_annual_units')
                    expected_launch_dates = self.data.get('expected_launch_date')
                    experience_types = self.data.get('experience_type')
                    experience_type_names = self.data.get('experience_type_name')
                    utm_campaigns = self.data.get('utm_campaign')
                    utm_contents = self.data.get('utm_content')
                    market_data_list = []
                    application_redirector_rules = []

                    product = Product.objects.create(
                        product_name=product_name,
                        brand=brand,
                        campaign_name=campaign,
                        product_description=product_description,
                        evrythng_tag_1=self.data.get('tag1')[0],
                        evrythng_tag_2=self.data.get('tag2')[0],
                        evrythng_tag_3=self.data.get('tag3')[0],
                        evrythng_tag_4=self.data.get('tag4')[0],
                        code_position=self.data.get('code_position')[0].strip(),
                        requested_by=self.data.get('requested_by')[0].strip(),
                        requested_date=datetime.strptime(self.data.get('date_requested')[0], "%Y-%m-%d").date(),
                        requester_email=self.data.get('requester_email')[0].strip(),
                        gs1_link=gs1_link
                    )
                    google_analytics = analytics_models.GoogleAnalytics.objects.create(
                        product=product,
                        brand=brand,
                        code_placement=self.data.get('code_placement')[0].strip(),
                        code_type=self.data.get('code_type')[0].strip(),
                        variant=self.data.get('variant')[0].strip() if self.data.get('variant')[0] else None,
                        campaign=campaign
                    )
                    for i in range(market_objs.count()):
                        if experience_types[i] == 'Other':
                            activity = Activity.objects.filter(experience_type=experience_type_names[i])
                            if not activity.exists():
                                activity = Activity.objects.create(
                                    experience_type=experience_type_names[i]
                                )
                            else:
                                activity = activity.first()
                        else:
                            activity = Activity.objects.get(id=experience_types[i])

                        if i == 0:
                            print(i)
                            print(market_objs[i])
                            product_market_details = ProductMarketDetails.objects.create(
                                product=product,
                                activity=activity,
                                is_default_market=True,
                                utm_campaign=utm_campaigns[i],
                                utm_content=utm_contents[i],
                                market=market_objs[i],
                                redirect_url=redirect_urls[i],
                                estimated_annual_units=estimated_annual_units[i],
                                expected_launch_date=expected_launch_dates[i],
                                utm_tagged_link=utm_tagged_links[i]
                            )
                            application_redirector_rules.append(
                                {
                                    "name": "Other",
                                    "redirectUrl": utm_tagged_links[i]
                                }
                            )
                        else:
                            print(market_objs[i])
                            print(i)
                            product_market_details = ProductMarketDetails.objects.create(
                                product=product,
                                activity=activity,
                                utm_campaign=utm_campaigns[i],
                                utm_content=utm_contents[i],
                                market=market_objs[i],
                                redirect_url=redirect_urls[i],
                                estimated_annual_units=estimated_annual_units[i],
                                expected_launch_date=expected_launch_dates[i],
                                utm_tagged_link=utm_tagged_links[i]
                            )
                            application_redirector_rules.append(
                                {
                                    "match": f"country={market_objs[i].market_iso_code}",
                                    "name": market_objs[i].market_name,
                                    "redirectUrl": utm_tagged_links[i]
                                }
                            )
                    default_market_data = application_redirector_rules.pop(0)
                    application_redirector_rules.append(default_market_data)
                    project_created, project_response = create_evrythng_project(
                        project_name=campaign_name
                    )
                    if project_created:
                        print('project created')
                        evrythng_project_id = project_response.json().get('id')
                        application_created, appllication_response = create_evrythng_project_application(
                            project_id=evrythng_project_id,
                            application_name=f'{product_name}_application'
                        )
                        if application_created:
                            print('application created')
                            evrythng_application_id = appllication_response.json().get('id')
                            product_created, product_response = create_evrythng_product(
                                tags=tags,
                                brand_name=local_brand.local_brand_name,
                                product_name=product_name,
                                product_description=product_description,
                                gtin=brand.upc_ean_gtin,
                                project_id=evrythng_project_id
                            )
                            if product_created:
                                print('product created')
                                evrythng_product_id = product_response.json().get('id')
                                redirection_created, redirection_response = create_evrythng_product_redirection(
                                    product_id=evrythng_product_id,
                                    default_redirect_url=utm_tagged_links[0]
                                )
                                if redirection_created:
                                    print('redirection created')
                                    short_id_link = SHORT_ID_LINK_FORMAT.format(redirection_response.json().get('shortId'))
                                    product.short_id = redirection_response.json().get('shortId')
                                    product.short_id_link=short_id_link
                                    product.save()
                                    gs1_qr_request_domain = os.environ.get("EVRYTHNG_QR_REQUEST_API_DOMAIN")
                                    qr_request_domain = os.environ.get("EVRYTHNG_SHORTID_QR_REQUEST_DOMAIN")
                                    if gs1_link:
                                        if gs1_qr_request_domain:
                                            product_qr_code_url = GS1_OR_CODE_LINK_FORMAT.format(gs1_qr_request_domain, brand.upc_ean_gtin, "default", 256, 256)
                                            product.qr_code_img_url = product_qr_code_url
                                            product.save()
                                        else:
                                            raise ImproperlyConfigured("Failed to find QR request domain.")
                                    else:
                                        if qr_request_domain:
                                            product_qr_code_url = OR_CODE_LINK_FORMAT.format(qr_request_domain, redirection_response.json()["shortId"])
                                            product.qr_code_img_url = product_qr_code_url
                                            product.save()   
                                        else:
                                            raise ImproperlyConfigured("Failed to find QR request domain.")

                                    customize_qr_product = product.id
                                    application_redirector_created, application_redirector_response = create_evrythng_application_level_redirector(
                                        project_id=evrythng_project_id,
                                        application_id=evrythng_application_id,
                                        rules=application_redirector_rules
                                    )
                                    if application_redirector_created:
                                        print('application redirector created')
                                        account_redirector_created, account_redirector_response = create_evrythng_account_level_redirector(
                                            name=f'{product.product_name} Redirector Rule',
                                            project_id=evrythng_project_id,
                                            application_id=evrythng_application_id,
                                            product_id=evrythng_product_id
                                        )
                                        if not account_redirector_created:
                                            success = False
                                            error_message = f"Failed to create evrythng account level redirector."
                                    else:
                                        success = False
                                        error_message = "Failed to create evrythng application level redirector."
                                else:
                                    success = False
                                    error_message = "Failed to create evrythng product redirection."
                            else:
                                success = False
                                error_message = "Failed to create evrythng product."
                        else:
                            success = False
                            error_message = "Failed to create evrythng project application."
                    else:
                        success = False
                        error_message = "Failed to create evrythng project."
                else:
                    success = False
                    error_message = "Product with given name already exists."
            else:
                success = False
                error_message = "Please provide brand code."

        except Exception as error:
            success = False
            error_message = str(error)
            print(error)

        finally:
            return success, error_message, customize_qr_product


class SalesDataForm(forms.ModelForm):
    # product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.Select(attrs={'class': 'form-select', 'id': 'product_input'}))
    actual_unit_sales = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'number', 'class': 'form-control', 'id': 'actual_unit_sales_input', 'onInput': 'show_product_existing_sales_data'}), required=False)
    estimated_unit_sales = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'number', 'class': 'form-control', 'id': 'estimated_unit_sales_input', 'onInput': 'show_product_existing_sales_data'}), required=False)
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'from_date_input', 'onChange': 'date_compare_func();', 'onInput':'show_product_existing_sales_data();'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'to_date_input', 'onChange': 'date_compare_func();', 'onInput':'show_product_existing_sales_data();'}))

    class Meta:
        model = SalesData
        fields = ['actual_unit_sales', 'estimated_unit_sales', 'from_date', 'to_date']

    def save(self, commit=False):
        if self.data.get('sales_data_id_input'):
            sales_data_obj = SalesData.objects.get(id=self.data.get('sales_data_id_input'))
            sales_data_obj.estimated_unit_sales = None
            sales_data_obj.actual_unit_sales = self.data.get('actual_unit_sales')
            sales_data_obj.save()
        else:
            instance = super(SalesDataForm, self).save(commit=False)
            product_obj = ProductMarketDetails.objects.get(id=self.data.get('product'))
            instance.product = product_obj
            instance.market = product_obj.market
            instance.save()


class PlanningDashboardDetailsForm(forms.ModelForm):
    forecast_attributed_incremental_sales_volume = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    purchase_price = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    activity = forms.ModelChoiceField(queryset=Activity.objects.all(), widget=forms.Select(attrs={"class": "form-select"}))
    local_brands = forms.ModelChoiceField(queryset=brand_models.LocalBrand.objects.all(), widget=forms.Select(attrs={"class": "form-select"}))
    brand = forms.ModelChoiceField(queryset=brand_models.Brand.objects.all(), widget=forms.Select(attrs={"class": "form-select"}))
    division = forms.ModelChoiceField(queryset=brand_models.Division.objects.all(), widget=forms.Select(attrs={"class": "form-select"}))
    market = forms.ModelChoiceField(queryset=Market.objects.all(), widget=forms.Select(attrs={"class": "form-select"}))
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.Select(attrs={"class": "form-select"}))
    products_category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
    product_salesdata = forms.ModelChoiceField(queryset=SalesData.objects.all(), widget=forms.Select(attrs={"class": "form-select"}))
    product_market_details = forms.ModelChoiceField(queryset=ProductMarketDetails.objects.all(), widget=forms.Select(attrs={"class": "form-select"}))
    cookie = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    data = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    dev_scans_data_4 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = PlanningDashboardDetails
        fields = '__all__'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields= '__all__'