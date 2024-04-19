import json
import datetime
from django import template
from django.db.models.base import ModelState
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def local_brands_queryset_as_json(qs):
    json_data_list = []
    for data in qs:
        json_data = {}
        json_data['pk'] = data.pk
        json_data['local_brand_name'] = data.local_brand_name
        # print(data.brand)
        try:
            json_data['brand_code'] = data.brand.brand_code
            # json_data['brand_name'] = data.brand.brand_name
        except AttributeError:
            pass
        finally:
            json_data_list.append(json_data)

    return mark_safe(json.dumps(json_data_list))


@register.filter
def product_queryset_as_json(qs):
    json_data_list = []
    for data in qs:
        json_data = {}
        for key, value in data.__dict__.items():
            if not isinstance(value, ModelState):
                if isinstance(value, datetime.date):
                    json_data[key] = value.strftime('%Y-%m-%d')
                else:
                    json_data[key] = value
        json_data['product_name'] = data.product.product_name
        json_data['market'] = data.market.market_name
        json_data_list.append(json_data)

    return mark_safe(json.dumps(json_data_list))


@register.filter
def sales_data_queryset_as_json(qs):
    json_data_list = []
    for data in qs:
        json_data = {}
        for key, value in data.__dict__.items():
            if not isinstance(value, ModelState):
                if isinstance(value, datetime.date):
                    json_data[key] = value.strftime('%Y-%m-%d')
                else:
                    json_data[key] = value
        json_data['main_product_id'] = data.product.product.id
        json_data['main_product_name'] = data.product.product.product_name
        json_data_list.append(json_data)

    return mark_safe(json.dumps(json_data_list))


@register.filter
def queryset_as_json(qs):
    json_data_list = []
    for data in qs:
        data.__dict__.pop('_state')
        json_data = data.__dict__
        for key, value in json_data.items():
            if isinstance(value, datetime.date):
                json_data[key] = value.strftime('%Y-%m-%d')
        json_data_list.append(json_data)

    return mark_safe(json.dumps(json_data_list))


@register.filter
def list_to_json(l):
    return mark_safe(json.dumps(l))
