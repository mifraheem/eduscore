from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role(*allowed_roles):
    """
    Role-based access decorator.

    Example usage:
    @login_required
    @role('teacher')
    def teacher_dashboard(...):

    or

    @login_required
    @role('teacher', 'student')
    def shared_view(...):
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Ensure user is authenticated
            if not request.user.is_authenticated:
                messages.error(request, "Please log in first.")
                return redirect(request.META.get('HTTP_REFERER', '/'))

            # Check if role is allowed
            user_role = getattr(request.user, 'role', None)
            if user_role not in allowed_roles:
                messages.error(request, "Access denied: You do not have permission to view this page.")
                # Redirect to previous page or home if no referrer
                return redirect(request.META.get('HTTP_REFERER', '/'))

            # Otherwise proceed normally
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
