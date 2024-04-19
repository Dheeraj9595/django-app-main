from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from .views import(
    admin_views,
    general_views
)


urlpatterns = [
    path('admin/auto_create_custom_groups/', admin_views.AutoCreateCustomGroups.as_view(), name='auto_create_custom_groups'),
    path('admin/logout/', admin_views.custom_logout),
    path('admin/', admin.site.urls),
    path('custom_admin_dashboard/', login_required(general_views.custom_admin_dashboard), name='custom_admin_dashboard'),
    path('reporting_view/', login_required(general_views.reporting_view), name='reporting_view'),
    path('qr_reporting_view/', login_required(general_views.qr_reporting_view), name='qr_reporting_view'),
    path('planning_view/', login_required(general_views.planning_view), name='planning_view'),
    path('manage_qr/', login_required(general_views.qr_manage_view), name='manage_qr'),
    path('accounts/', include('allauth.urls')),
    path('products/', include('products.urls')),
    path('campaigns/', include('campaigns.urls')),
    path('qr_code_templates/', general_views.qr_code_templates_view, name='qr_code_templates'),
    path('save_qr_customization_template/', general_views.save_qr_customization_template_view, name='save_qr_customization_template')
]
urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)