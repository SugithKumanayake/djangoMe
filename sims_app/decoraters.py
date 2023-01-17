from django.http import HttpResponse
from django.shortcuts import redirect

def unathenticated_user(function_in_view):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return function_in_view(request, *args, **kwargs)
    return wrapper_function