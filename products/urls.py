from django.urls import path

from .views import(
    QRRequestFormView,
    SalesDataFormView,
    QRTemplateApplyView,
    QRCodeCustomizeView,
    PlanningDashboardFormView,
    ProductView
)


urlpatterns = [
    path('qr_request_form/', QRRequestFormView.as_view(), name="qr_request_form"),
    path('sales_data_form/', SalesDataFormView.as_view(), name='sales_data_form'),
    path('qr_code_customize_form/', QRCodeCustomizeView.as_view(), name='qr_code_customize_form'),
    path('planning_dashboard_details_form/', PlanningDashboardFormView.as_view(), name='planning_dashboard_details_form'),
    path('qr_template_apply_form/', QRTemplateApplyView.as_view(), name='qr_template_apply_form'),
    path('products/',ProductView.as_view(),name='productview')
]