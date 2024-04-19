from django.contrib.auth.mixins import LoginRequiredMixin

class AdminLoginRequiredMixin(LoginRequiredMixin):
    
    def dispatch(self, request, *args, **kwargs):
        """
        Check if the user is logged in and is a superuser
        """
        if not request.user.is_authenticated or not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
