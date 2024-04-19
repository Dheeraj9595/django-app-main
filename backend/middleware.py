from django.shortcuts import redirect


class CustomAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/':
            return redirect('custom_admin_dashboard')
        elif request.path == '/admin/':
            return redirect('custom_admin_dashboard')

        response = self.get_response(request)
        return response
