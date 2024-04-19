import os
import io
import time
import requests
from PIL import Image
from django.core.files import File
from azure.storage.blob import BlobServiceClient, BlobClient

from .constants import(
    QR_CODE_BLOB_STORAGE_CONTAINER_NAME,
    QR_CODE_BLOB_STORAGE_CONNECTION_STRING
)
from .models import Product, QRCodeCutomizationTemplates


def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    rgb = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    return rgb


def upload_qr_to_blob(file_obj, filename):
    connection_string = QR_CODE_BLOB_STORAGE_CONNECTION_STRING
    container_name = QR_CODE_BLOB_STORAGE_CONTAINER_NAME
    # file_path = "test_img_new.png"
    file_stream = io.BytesIO(file_obj)
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    # with open(file_path, "rb") as data:
    blob_client.upload_blob(file_stream)
    print("File uploaded successfully!", blob_client.url)
    return blob_client.url


def upload_qr_code_logo_img(img_file):
    success = False
    filename = None
    try:
        url = os.getenv('QR_MONKEY_API_BASE_URL')
        url+="/qr/uploadimage"
        file_dict = {'file': img_file}
        response = requests.post(url=url, files=file_dict)
        if response.status_code == 200:
            filename = response.json().get('file')
            success = True
        else:
            print(response.text)
    except Exception as error:
        success=False
        print(error)
    finally:
        return success, filename


def customize_qr_code(color, eye_shape, product_id, qr_code_logo_img_name=None, img_name=None, qr_code_logo_img=None, bgColor=None):
    product = None
    try:
        product = Product.objects.get(id=product_id)
        url = os.getenv('QR_MONKEY_API_BASE_URL')
        url+='/qr/custom'
        if product.gs1_link:
            product_url = product.gs1_link
        else:
            product_url = product.short_id_link
        if not bgColor or bgColor == '#000000':
            bgColor = "#FFFFFF"

        json_data = {
        "data": product_url,
        "config": {
            "body": "square",
            "eye": eye_shape,
            "eyeBall": "ball0",
            "erf1": [],
            "erf2": [],
            "erf3": [],
            "brf1": [],
            "brf2": [],
            "brf3": [],
            "bodyColor": color,
            "bgColor": bgColor,
            "eye1Color": color,
            "eye2Color": color,
            "eye3Color": color,
            "eyeBall1Color": color,
            "eyeBall2Color": color,
            "eyeBall3Color": color,
            "gradientColor1": "",
            "gradientColor2": "",
            "gradientType": "linear",
            "gradientOnEyes": "true",
            "logoMode": "default"
        },
        "size": 180,
        "download": True,
        "file": "png"
        }

        qr_logo_filename = None
        if qr_code_logo_img:
            qr_logo_upload_success, qr_logo_filename = upload_qr_code_logo_img(qr_code_logo_img)
            if qr_logo_upload_success:
                json_data['config']['logo'] = qr_logo_filename
        elif qr_code_logo_img_name:
            json_data['config']['logo'] = qr_code_logo_img_name

        response = requests.post(url=url, json=json_data)
        print(response.status_code)
        if response.status_code == 200:
            img_url = 'https:' + response.json()['imageUrl']
            if product.gs1_link:
                img_name = f'{product.product_name}_{product.brand.upc_ean_gtin}_{int(time.time())}.png'
            else:
                img_name = f'{product.product_name}_{product.short_id}_{int(time.time())}.png'

            image_resp = requests.get(img_url)
            if image_resp.status_code == 200:
                uploaded_qr_code_url = upload_qr_to_blob(image_resp.content, img_name)
                product.customized_qr_code_img_blob_url = uploaded_qr_code_url
                product.save()
                qr_customization_response_template = {
                    "qr_code_color":color,
                    "qr_code_eye_shape":eye_shape,
                    "qr_code_background_color":bgColor,
                    "qr_code_img_url":uploaded_qr_code_url,
                    "qr_code_logo_image":qr_logo_filename
                }
                return qr_customization_response_template
            else:
                return {}
        else:
            return {}
    except Exception as error:
        print(error)
        return {}


# def customize_qr_code(color, img_name, qr_code_logo_img):
    # color = hex_to_rgb(color)
    # qr_img = Image.open(f'./backend/media/products_qr_codes/{img_name}')
    # qr_img = qr_img.convert("L")

    # qr_img = qr_img.convert("RGB")
    # qr_img = qr_img.convert("P", palette=Image.ADAPTIVE, colors=2)
    # qr_img.putpalette([255, 255, 255, color[0], color[1], color[2]])

    # logo_img = Image.open(qr_code_logo_img)
    # qr_width, qr_height = qr_img.size
    # logo_width, logo_height = logo_img.size
    # logo_size = int(qr_width * 0.2)
    # logo_img = logo_img.resize((logo_size, logo_size))
    # logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

    # eye_img = Image.open('./backend/media/products_qr_codes/eye_two.png').convert("RGBA").resize((logo_size, logo_size))
    # qr_img.paste(eye_img, logo_position, mask=eye_img)

    # qr_with_logo = Image.new('RGBA', (qr_width, qr_height), (255, 255, 255, 255))
    # qr_with_logo.paste(qr_img, (0, 0))
    # qr_with_logo.paste(logo_img, logo_position, mask=logo_img)
    
    # img_name = '_'.join(img_name.split('_')[-2:])
    # img_name = f'processed_{int(time.time())}_{img_name}'
    # img_path = f"./backend/media/products_qr_codes/{img_name}"

    # qr_with_logo.save(img_path)
    # return img_name


# def customize_qr_code(color, img_name, qr_code_logo_img):
#     color = hex_to_rgb(color)
#     qr_img = Image.open(f'./backend/media/products_qr_codes/{img_name}')
#     qr_img = qr_img.convert("L")

#     qr_img = qr_img.convert("RGB")
#     qr_img = qr_img.convert("P", palette=Image.ADAPTIVE, colors=2)
#     qr_img.putpalette([255, 255, 255, color[0], color[1], color[2]])

#     logo_img = Image.open(qr_code_logo_img)
#     qr_width, qr_height = qr_img.size
#     logo_width, logo_height = logo_img.size
#     logo_size = int(qr_width * 0.2)
#     logo_img = logo_img.resize((logo_size, logo_size))
#     logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

#     eye_img = Image.open('./backend/media/products_qr_codes/eye_two.png').convert("RGBA").resize((logo_size, logo_size))
#     qr_img.paste(eye_img, logo_position, mask=eye_img)

#     qr_with_logo = Image.new('RGBA', (qr_width, qr_height), (255, 255, 255, 255))
#     qr_with_logo.paste(qr_img, (0, 0))
#     qr_with_logo.paste(logo_img, logo_position, mask=logo_img)
    
#     img_name = '_'.join(img_name.split('_')[-2:])
#     img_name = f'processed_{int(time.time())}_{img_name}'
#     img_path = f"./backend/media/products_qr_codes/{img_name}"

#     qr_with_logo.save(img_path)
#     return img_name
