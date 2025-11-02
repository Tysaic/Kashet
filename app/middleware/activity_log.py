from app.models import ActivityLog
from django.utils.deprecation import MiddlewareMixin


class ActivityLogMiddleware(MiddlewareMixin):

    """
    Middleware to registry logs of users or anonymous activities in app application.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        
        if request.method in ('GET', 'HEAD', 'OPTIONS'):

            return None
        
        #user = request.user if request.user.is_authenticated else None

        if hasattr(view_func, "view_class"):
            view_name = f"{view_func.view_class.__module__}.{view_func.view_class.__name__}"
        else:
            view_name = f"{view_func.__module__}.{view_func.__name__}"
        ip = request.META.get("REMOTE_ADDR")

        ActivityLog.objects.create(
            #user = user,
            level = 'INFO',
            action = view_name,
            method = request.method,
            path = request.path,
            ip_address = ip,
        )
        return None