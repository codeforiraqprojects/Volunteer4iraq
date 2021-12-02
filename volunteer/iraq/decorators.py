from django.shortcuts import redirect



def notLoggedUsers(view_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/admin_home')
        else:
            return view_func(request,*args, **kwargs)
    return wrapper_func


def allowedUsers(allowedGroups=[]):
    def decorator(view_func):
        def wrapper_func(request,*args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all[0].name()
            if group in allowedGroups:
                return view_func(request,*args, **kwargs)
            else:
                return redirect('/profile')
        return wrapper_func 
    return decorator 



def IntityAdmins(view_func):
        def wrapper_func(request,*args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all[0].name()
            if group == 'intityAdmin':
                return view_func(request,*args, **kwargs)
            if group == 'user':
                return redirect('/profile')
        return wrapper_func 
