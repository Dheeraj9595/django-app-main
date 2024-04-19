from .forms import ORRequestForm
from backend.celery import app as celery_app


@celery_app.task(name='submit_qr_request_form')
def submit_qr_request_form(form_data, form_number):
    form = ORRequestForm(form_data)
    success, error_message, customize_qr_product = form.save()
    return success, error_message, form_number, customize_qr_product
