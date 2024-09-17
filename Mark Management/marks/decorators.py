# from django.http import HttpResponseForbidden

# def admin_required(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         if request.user.role != 'ADMIN':
#             print(request.user.role)
#             return HttpResponseForbidden("You do not have permission to access this page.")
#         return view_func(request, *args, **kwargs)
#     return wrapper_func



from django.http import HttpResponseForbidden
from functools import wraps

def permission_required(permission):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request.user, permission) or not getattr(request.user, permission):
                return HttpResponseForbidden("You do not have permission to access this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

can_add_required = permission_required('can_add')
can_update_required = permission_required('can_update')
can_delete_required = permission_required('can_delete')
