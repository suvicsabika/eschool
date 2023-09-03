from functools import wraps
from django.shortcuts import redirect

def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'Teacher':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('access_denied')  # Redirect to an access denied page or handle accordingly
    return _wrapped_view
