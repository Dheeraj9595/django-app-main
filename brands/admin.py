from django.contrib import admin
from .models import (
    Brand,
    Division,
    LocalBrand
)


admin.site.register(Brand)
admin.site.register(Division)
admin.site.register(LocalBrand)
