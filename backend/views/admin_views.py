from django.views import View
from django.contrib.auth import logout
from django.shortcuts import(
    render,
    redirect
)
from django.contrib.auth.models import(
    Group,
    Permission
)
from django.contrib.contenttypes.models import ContentType

from ..mixins import AdminLoginRequiredMixin
from ..constants import (
    VIEWER_ACCESS_GRP_NAME,
    CAMPAIGN_ACCESS_GRP_NAME,
    SUPERUSER_ACCESS_GRP_NAME
)


def custom_logout(request):
    """
        Custom Admin Logout View
    """
    logout(request)
    return render(request, 'custom_logout.html')


class AutoCreateCustomGroups(AdminLoginRequiredMixin, View):
    """
        Auto Create Custom Groups Views
    """
    def get(self, request):
        superuser_grp = Group.objects.filter(name=SUPERUSER_ACCESS_GRP_NAME)
        user_grp = Group.objects.filter(name=CAMPAIGN_ACCESS_GRP_NAME)
        staff_grp = Group.objects.filter(name=VIEWER_ACCESS_GRP_NAME)
        all_perms = Permission.objects.all()
        custom_content_types = ContentType.objects.exclude(
            app_label__in=['auth', 'account', 'admin', 'contenttypes', 'sessions', 'sites', 'socialaccount', 'user_additional_details']
        )
        user_perms = all_perms.filter(content_type__in=custom_content_types)
        staff_perms = user_perms.filter(codename__startswith='view_')
        if not superuser_grp.exists():
            superuser_grp = Group.objects.create(
                name=SUPERUSER_ACCESS_GRP_NAME
            )
            superuser_grp.permissions.add(*all_perms)
        if not user_grp.exists():
            user_grp = Group.objects.create(
                name=CAMPAIGN_ACCESS_GRP_NAME
            )
            user_grp.permissions.add(*user_perms)
        if not staff_grp.exists():
            staff_grp = Group.objects.create(name=VIEWER_ACCESS_GRP_NAME)
            staff_grp.permissions.add(*staff_perms)

        return redirect('/admin/auth/group/')
