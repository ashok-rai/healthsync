from django.http import HttpResponseForbidden

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.path.startswith('/doctor/') and request.user.role != 'Doctor':
                return HttpResponseForbidden("Access denied.")
            if request.path.startswith('/admin/') and request.user.role != 'Admin':
                return HttpResponseForbidden("Access denied.")
        response = self.get_response(request)
        return response