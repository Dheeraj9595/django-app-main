from django.views import View
from datetime import datetime
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.forms import formset_factory

from brands import models as brand_models
from .tasks import submit_qr_request_form
from campaigns import models as campaign_models
from backend.mixins import AdminLoginRequiredMixin
from .models import(
    Market,
    Product,
    Activity,
    SalesData,
    ProductMarketDetails,
    QRCodeCutomizationTemplates
)
from .forms import(
    ORRequestForm,
    SalesDataForm, 
    PlanningDashboardDetailsForm,
    ProductForm
)
from .utils import customize_qr_code
import json 


class QRRequestFormView(AdminLoginRequiredMixin, View):
    """
        QR Request Form Views
    """
    formset_class = formset_factory(ORRequestForm, extra=1)

    def get(self, request):

        campaign_id = request.GET.get('campaign_id')
        selected_market = request.GET.get('market')
        exp_launch_date = request.GET.get('launch_date')
        try:
            selected_campaign = campaign_models.Campaign.objects.get(id = campaign_id)
            campaigns = campaign_models.Campaign.objects.all()
            selected_market = Market.objects.get(market_name=request.GET.get('market'))
            markets = Market.objects.all()
        except:
            campaigns = campaign_models.Campaign.objects.all()
            selected_campaign = None
            markets = Market.objects.all()

        local_brands = brand_models.LocalBrand.objects.all().exclude(brand=None)
        brands = brand_models.Brand.objects.all()
        activities = Activity.objects.all()
        products = Product.objects.all()
        current_date = datetime.now().date().strftime('%Y-%m-%d')
        formset = self.formset_class()
        return render(request, 'qr_request_form.html', {"formset": formset, "campaign_id": campaign_id, "local_brands": local_brands, "brands": brands, "activities": activities, "products": products, "markets": markets, "current_date": current_date,'selected_campaign' : selected_campaign, "campaigns":campaigns,"selected_market":selected_market,"expected_lauch_date":exp_launch_date})
        
        
    def post(self, request):
        print('form_submitted')
        success = False
        error_message = None
        formset = self.formset_class(request.POST)
        celery_tasks = []
        tasks_results = []
        # print(formset.total_form_count())
        # print(formset.is_valid())
        formset_error_message = None
        customize_qr_products_list = []
        if formset.is_valid():
            for i in range(formset.total_form_count()):
                form_data = {key.replace(f'form-{i}-', ''): formset.data.getlist(key) for key in formset.data.keys() if f'form-{i}-' in key}
                print(i%2==0)
                if i%2==0:
                    form = ORRequestForm(form_data)
                    success, error_message, customize_qr_product = form.save()
                    print(success)
                    if not success:
                        tasks_results.append(
                            {
                                'form': i+1,
                                'error_message': error_message
                            }
                        )
                    else:
                        customize_qr_products_list.append(customize_qr_product)
                else:
                    task = submit_qr_request_form.delay(form_data, i+1)
                    celery_tasks.append(task)
                 
            while True:
                if all(task.ready() for task in celery_tasks):
                    for task in celery_tasks:
                        if not task.result[0]:
                            tasks_results.append(
                                {
                                    'form': task.result[2],
                                    'error_message': task.result[1]
                                }
                            )
                        else:
                            customize_qr_products_list.append(task.result[3])
                    break
        else:
            formset_error_message = formset.errors
            print(formset_error_message)
        
        print(tasks_results)
        if formset_error_message:
            messages.error(request, f'Failed to submit QR request form - {formset_error_message}')
            return redirect('/products/qr_request_form')
        elif bool(len(tasks_results)):
            messages.error(request, f'Failed to submit QR request form - {tasks_results}')
            return redirect('/products/qr_request_form')
        else:
            customize_qr_product_id = customize_qr_products_list[-1]
            qr_customize_form_url = reverse('qr_code_customize_form') + f'?product_id={customize_qr_product_id}'
            messages.success(request, 'QR request form submitted successfully.')
            return redirect(qr_customize_form_url)
            # return redirect('/products/qr_code_customize_form')


class SalesDataFormView(AdminLoginRequiredMixin, View):
    """
        Sales Data Form Views
    """
    def get(self, request):
        campaign_id = request.GET.get('campaign_id')
        if campaign_id:
            campaign_additional_details_objs = campaign_models.CampaignAdditionalDetails.objects.filter(campaign__id=campaign_id)
            if campaign_additional_details_objs.exists():
                product_ids = campaign_additional_details_objs.values_list('product_name', flat=True)
            else:
                product_ids = []
            product_market_details_objs = ProductMarketDetails.objects.filter(product__id__in=product_ids)
        else:
            product_market_details_objs = ProductMarketDetails.objects.all()
        form = SalesDataForm()
        sales_data_objs = SalesData.objects.all()
        market_objs = Market.objects.all()
        return render(request, 'products/sales_data_form.html', {'form': form, 'sales_data_objs': sales_data_objs, 'market_objs': market_objs, 'product_objs': product_market_details_objs, 'campaign_id': campaign_id})

    def post(self, request):
        campaign_id = request.POST.get('campaign_id')
        # campaign_list_url = reverse('campaigns:campaign_list')
        campaign_detail_form_url = reverse('admin:campaigns_campaign_change', args=(campaign_id,))
        form = SalesDataForm(request.POST)
        if form.is_valid():
            form.save()
            if campaign_id is not None and campaign_id != 'None':
                return redirect(campaign_detail_form_url)
            else:
                messages.success(request, 'Sales data form submitted successfully.')
        else:
            error_message = form.errors.as_json()
            messages.error(request, f'Failed to submit Sales data form - {error_message}')
        return redirect('/admin/campaigns/campaign/')


class QRCodeCustomizeView(AdminLoginRequiredMixin, View):
    """
        QR Code Customize Views
    """
    def get(self, request):
        chosen_product_id = request.GET.get('product_id')
        products = Product.objects.exclude(qr_code_img_url=None)
        return render(request, 'products/qr_code_customize_form.html', {'products': products, 'chosen_product_id': chosen_product_id})

    # def post(self, request):
    #     request_data = json.loads(request.body.decode('utf-8'))
    #     print(request_data)
    #     image_name = request_data['qr_code_image_url'].split('/')[-1]
    #     image_name = customize_qr_code(
    #         color=request_data['color'],
    #         img_name=image_name
    #     )
    #     image_url = f'/media/products_qr_codes/{image_name}'
    #     response_data = {'image_url': image_url}
    #     return JsonResponse(response_data)

    def post(self, request):
        product_id = request.POST.get('qr_code_product_id')
        image_name = request.POST.get('qr_code_image_src').strip()
        if image_name and bool(len(image_name)):
            image_name = image_name.split('/')[-1]
        else:
            image_name = None
            print('QR code image src not found')
            return JsonResponse({})

        eye_shape = request.POST.get('eye_shape')
        bgColor = request.POST.get('bgColor')
        qr_code_color = request.POST['qr_code_color']
        qr_customization_response_template = customize_qr_code(
            color=qr_code_color,
            img_name=image_name,
            eye_shape=eye_shape,
            qr_code_logo_img=request.FILES.get('qr_code_logo_image'),
            bgColor=bgColor,
            product_id=product_id
        )
        return JsonResponse(qr_customization_response_template)


class QRTemplateApplyView(AdminLoginRequiredMixin, View):
    """
        QR Template Apply Form Views
    """
    def post(self, request):
        qr_template = QRCodeCutomizationTemplates.objects.get(id=request.POST.get('template_apply_id'))
        product_id = request.POST.get('template_apply_product')
        product = Product.objects.get(id=product_id)
        qr_customization_response_template = customize_qr_code(
            color=qr_template.qr_code_color,
            eye_shape=qr_template.qr_code_eye_shape,
            qr_code_logo_img_name=qr_template.qr_code_logo_image,
            bgColor=qr_template.qr_code_background_color,
            product_id=product.id
        )
        messages.success(request, f"Template applied successfully on product - {product.product_name}")
        return redirect('/custom_admin_dashboard')


class PlanningDashboardFormView(AdminLoginRequiredMixin, View):
    """
        Planning Dashboard Form Views
    """
    def get(self, request):
        form = PlanningDashboardDetailsForm()
        return render(request, 'products/planning_dashboard_details_form.html', {'form': form})

    def post(self, request):
        form = PlanningDashboardDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Planning Dashboard Details form submitted successfully.')
        else:
            error_message = form.errors.as_json()
            messages.error(request, f'Failed to submit Planning Dashboard Details form - {error_message}')        
        return redirect('/custom_admin_dashboard')


class ProductView(View):
    def post(self,request):
        data = request.body
        json_string = data.decode('utf-8')
        json_data = json.loads(json_string)
        form = ProductForm(json_data)
        if form.is_valid():
            product = form.save()
            print(product)
            return JsonResponse({'product_id':product.id})
        else:
            error_message = form.errors.as_json()
            messages.error(request, f'Failed to submit Product form - {error_message}')
            return redirect('/qr_code_templates/')