from django.http import HttpResponse
from django.shortcuts import redirect

def unathenticated_user(function_in_view):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return function_in_view(request, *args, **kwargs)
    return wrapper_function

def allowed_users(allowed_roles=[]):
    def decorater(view_function):
        def wrapper_function(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_function(request, *args, **kwargs)
            else:
                return HttpResponse("Sorry! admin can only view this page")
        return wrapper_function
    return decorater

def reg_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'admin' or group == 'user':
            return view_function(request, *args, **kwargs)
        else:
            return redirect('register')
            
    return wrapper_function