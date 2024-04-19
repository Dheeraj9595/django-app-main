from django.contrib import messages
from django.shortcuts import render, redirect
from backend import constants

from products import models as product_models


def custom_admin_dashboard(request):
    """
        Custom Admin Dashboard View
    """
    if request.method=='GET':
        return render(request, 'custom_admin_dashboard.html')


def qr_reporting_view(request):
    """
        Reporting View
    """
    if request.method=='GET':
        iframe = constants.QR_CODE_PERFORMANCE_REPORT
        return render(request, 'qr_reporting.html', context={'iframe_src': iframe})


def reporting_view(request):
    """
        QR Reporting View
    """
    if request.method=='GET':
        iframe = constants.CONNECTED_PACK_REPORT
        return render(request, 'reporting.html', context={'iframe_src': iframe})


def planning_view(request):
    """
        Planning View
    """
    if request.method=='GET':
        iframe = constants.PLANNING_REPORT
        return render(request, 'planning.html', context={'iframe_src': iframe})


def qr_manage_view(request):
    """
        QR Manage View
    """
    if request.method == 'GET':
        iframe = constants.QR_CODE_PERFORMANCE_REPORT
        return render(request, 'manage_qr.html', context={'iframe_src': iframe})


def qr_code_templates_view(request):
    print('request to templates received')
    if request.method == 'POST':
        qr_code_template = product_models.QRCodeCutomizationTemplates.objects.create(
            template_name=request.POST.get('qr_code_template_name'),
            qr_code_color=request.POST.get('qr_code_template_color'),
            qr_code_eye_shape=request.POST.get('qr_code_template_eye_shape'),
            qr_code_background_color=request.POST.get('qr_code_template_background_color'),
            qr_code_logo_image=request.POST.get('qr_code_template_logo_image'),
            sample_qr_code_blob_url=request.POST.get('qr_code_template_img_url'),
        )
    else:
        data = request.GET
        try:
            products = product_models.Product.objects.filter(id = data.get('product_name'))
        except:
            products = product_models.Product.objects.exclude(qr_code_img_url=None)
        qr_code_templates = product_models.QRCodeCutomizationTemplates.objects.all()
        return render(request, 'qr_code_templates.html', {'products': products, 'qr_code_templates': qr_code_templates})


def save_qr_customization_template_view(request):
    """
        Save QR Customization Template View
    """
    if request.method=='GET':
        messages.success(request, 'QR Customization template saved successfully.')
        return redirect('/qr_code_templates')
