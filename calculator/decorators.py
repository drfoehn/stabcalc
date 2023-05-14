from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    #create user roles in admin: "admin", "manager", "labuser"
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.users.groups.exists():
                group = request.users.groups.all()[0].name
            if group in allowed_roles:


                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page")
        return wrapper_func
    return decorator


def only_for_staff(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/')

    return wrapper_func

def owner_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper_func


