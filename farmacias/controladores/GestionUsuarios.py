from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied("Debes iniciar sesión")
            if request.user.cargo not in allowed_roles:
                messages.error(request, 'No tienes permisos para acceder a esta página.')
                return redirect(f'inicio_{request.user.cargo}')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator



def login_view(request):
    
    next_url = request.GET.get('next', 'inicio_publico')  
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect(next_url) 
        else:
            messages.error(request, 'Credenciales inválidas. Intenta de nuevo.')
    
    return render(request, 'login.html')


