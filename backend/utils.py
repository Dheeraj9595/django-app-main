import os
import requests
from io import BytesIO
from django.core.files import File

from .constants import OR_CODE_API_LINK_FORMAT


def create_evrythng_project(project_name):
    success = False
    response = None
    request_url = os.environ.get('EVRYTHNG_API_URL')
    access_token = os.environ.get('EVRYTHNG_API_ACCESS_TOKEN')
    if request_url:
        request_url = request_url+'projects'
        if access_token:
            headers = {
                "content-type":"application/json",
                "authorization":access_token
            }
            json_data = {
                "name": project_name
            }
            response = requests.post(url=request_url, headers=headers, json=json_data)
            if response.status_code == 201 and 'id' in response.json():
                success = True
            else:
                print(response.text)
        else:
            print("Access token not found")
    else:
        print("Request domain not found")

    return success, response


def create_evrythng_project_application(project_id, application_name):
    success = False
    response = None
    request_url = os.environ.get('EVRYTHNG_API_URL')
    access_token = os.environ.get('EVRYTHNG_API_ACCESS_TOKEN')
    if request_url:
        request_url = request_url+f'projects/{project_id}/applications'
        if access_token:
            headers = {
                "content-type":"application/json",
                "authorization":access_token
            }
            json_data = {
                "name": application_name,
                "socialNetworks": {}
            }
            response = requests.post(url=request_url, headers=headers, json=json_data)
            if response.status_code == 201 and 'id' in response.json():
                success = True
            else:
                print(response.text)
        else:
            print("Access token not found")
    else:
        print("Request domain not found")

    return success, response


def create_evrythng_product(tags, brand_name, product_name, product_description, gtin, project_id):
    '''
       Creates an evrythng product
    '''
    success = False
    response = None
    request_url = os.environ.get('EVRYTHNG_API_URL')
    access_token = os.environ.get('EVRYTHNG_API_ACCESS_TOKEN')
    if request_url:
        request_url = request_url+f'products?project={project_id}'
        if access_token:
            headers = {
                "content-type":"application/json",
                "authorization":access_token
            }
            json_data = { 
                "tags":tags,
                "brand":brand_name,
                "name":product_name,
                "description":product_description,
                "identifiers":{"gs1:01":gtin}
                }
            response = requests.post(url=request_url, headers=headers, json=json_data)
            print(response.status_code)
            if response.status_code == 201 and 'id' in response.json():
                success = True
                # response_data = response.json()
            else:
                print(response.text)
        else:
            print("Access token not found")
    else:
        print("Request domain not found")
    
    return success, response


def create_evrythng_product_redirection(product_id, default_redirect_url):
    '''
       Creates the evrythng product redirection by product id
    '''
    success = False
    response = {}
    request_url = os.environ.get('EVRYTHNG_REDIRECTION_API_DOMAIN')
    access_token = os.environ.get('EVRYTHNG_API_ACCESS_TOKEN')
    if request_url:
        request_url = request_url+f'products/{product_id}/redirector'
        if access_token:
            default_redirect_url += '?productId={productId}'
            headers = {
                "content-type":"application/json",
                "authorization":access_token
            }
            json_data = {
                "defaultRedirectUrl": default_redirect_url
            }
            response = requests.post(url=request_url, headers=headers, json=json_data)
            print(response.status_code)
            if response.status_code == 201 and 'shortId' in response.json():
                success = True
                # response_data = response.json()
            else:
                print(response.text)
        else:
            print("Access token not found")
    else:
        print("Request domain not found")
    
    return success, response


def create_evrythng_application_level_redirector(project_id, application_id, rules):
    '''
       Creates the evrythng product redirection by product id
    '''
    success = False
    response = {}
    request_url = os.environ.get('EVRYTHNG_REDIRECTION_API_DOMAIN')
    access_token = os.environ.get('EVRYTHNG_API_ACCESS_TOKEN')
    if request_url:
        request_url = request_url+f'projects/{project_id}/applications/{application_id}/redirector'
        if access_token:
            headers = {
                "content-type":"application/json",
                "authorization":access_token
            }
            json_data = {
                "rules": rules
            }
            response = requests.put(url=request_url, headers=headers, json=json_data)
            print(response.status_code)
            if response.status_code == 200:
                success = True
                # response_data = response.json()
            else:
                print(response.text)
        else:
            print("Access token not found")
    else:
        print("Request domain not found")

    return success, response


def get_existing_evrythng_account_level_redirector():
    '''
       Fetches existing evrythng account level redirector
    '''
    success = False
    response = None
    existing_rules = []
    request_url = os.environ.get('EVRYTHNG_API_URL')
    access_token = os.environ.get('EVRYTHNG_API_ACCESS_TOKEN')
    if request_url:
        request_url = request_url+'redirector'
        if access_token:
            headers = {
                "content-type":"application/json",
                "authorization":access_token
            }
            response = requests.get(url=request_url, headers=headers)
            print(response.status_code)
            if response.status_code == 200 and 'rules' in response.json():
                success = True
                existing_rules = response.json()['rules']
            else:
                print(response.text)
        else:
            print("Access token not found")
    else:
        print("Request domain not found")
    
    return success, existing_rules


def create_evrythng_account_level_redirector(name, project_id, product_id, application_id):
    '''
       Creates the evrythng product redirection by product id
    '''
    success = False
    response = {}
    request_url = os.environ.get('EVRYTHNG_REDIRECTION_API_DOMAIN')
    access_token = os.environ.get('EVRYTHNG_API_ACCESS_TOKEN')
    if request_url:
        request_url = request_url+f'redirector'
        if access_token:
            rules_list = []
            existing_rules_found, existing_rules = get_existing_evrythng_account_level_redirector()
            if existing_rules_found:
                rules_list.extend(existing_rules)
            rules_list.extend(
                [
                    {
                        "match": f"product.id={product_id}",
                        "name": name,
                        "delegates": [{
                            "app": application_id,
                            "project": project_id
                        }]
                    }
                ]
            )
            headers = {
                "content-type":"application/json",
                "authorization":access_token
            }
            # json_data = {
            #     "rules": [{
            #         "match": f"product.id={product_id}",
            #         "name": name,
            #         "delegates": [{
            #             "app": application_id,
            #             "project": project_id
            #         }]
            #     }]
            # }
            json_data = {
                "rules": rules_list
            }
            response = requests.put(url=request_url, headers=headers, json=json_data)
            print(response.status_code)
            if response.status_code == 200:
                success = True
                # response_data = response.json()
            else:
                print(response.text)
        else:
            print("Access token not found")
    else:
        print("Request domain not found")

    return success, response


def generate_evrythng_qr_code(gtin, product, tpl='default', width=256, height=256):
    '''
       Generates and saves GS1 link encoded QR code for a product's redirection
    '''
    success = False
    request_url = os.environ.get('EVRYTHNG_QR_REQUEST_API_DOMAIN')
    if request_url:
        request_url = OR_CODE_API_LINK_FORMAT.format(request_url, gtin, tpl, width, height)
        headers = {
            "accept":"image/png"
        }
        response = requests.get(url=request_url, headers=headers)
        # print(response.status_code)
        if response.status_code == 200:
            file_name = f'{product.product_name}_{gtin}_qr.png'
            image_data = BytesIO(response.content)
            image_file = File(image_data)
            product.qr_code_img.save(file_name, image_file, save=True)
            product.save()
            print('Image saved sucessfully Downloaded: ', file_name)
            success = True
        else:
            print(response.text)
    else:
        print("Request domain not found")

    return success, product


# def generate_evrythng_qr_code(gtin, product, tpl='default', width=256, height=256):
#     '''
#        Generates and saves GS1 link encoded QR code for a product's redirection
#     '''
#     success = False
#     request_url = os.environ.get('EVRYTHNG_QR_REQUEST_API_DOMAIN')
#     if request_url:
#         request_url = OR_CODE_API_LINK_FORMAT.format(request_url, gtin, tpl, width, height)
#         headers = {
#             "accept":"image/png"
#         }
#         response = requests.get(url=request_url, headers=headers)
#         print(response.status_code)
#         if response.status_code == 200:
#             file_name = f'{product.product_name}_{gtin}_qr.png'
#             with open(file_name, 'wb') as f:
#                 f.write(response.content)
#                 print('Image sucessfully Downloaded: ', file_name)
#             success = True
#         else:
#             print(response.text)
#     else:
#         print("Request domain not found")

#     return success


# def create_evrythng_product_redirection(evrythng_id, default_redirect_url):
#     '''
#        Creates the evrythng product redirection by product id
#     '''
#     success = False
#     response = {}
#     request_url = os.environ.get('EVRYTHNG_REDIRECTION_API_DOMAIN')
#     access_token = os.environ.get('EVRYTHNG_API_ACCESS_TOKEN')
#     if request_url:
#         request_url = request_url+'redirections'
#         if access_token:
#             headers = {
#                 "content-type":"application/json",
#                 "authorization":access_token,
#                 "accept":"application/json"
#             }
#             json_data = {
#                 "type": "product",
#                 "evrythngId": evrythng_id,
#                 "defaultRedirectUrl": default_redirect_url
#                 }
#             response = requests.post(url=request_url, headers=headers, json=json_data)
#             print(response.status_code)
#             if response.status_code == 201 and 'shortId' in response.json():
#                 success = True
#                 # response_data = response.json()
#             else:
#                 print(response.text)
#         else:
#             print("Access token not found")
#     else:
#         print("Request domain not found")

#     return success, response
