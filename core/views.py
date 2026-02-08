from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
import re

def home(request):
    return render(request, 'core/index.html')

def crear_cuenta(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        
        errors = []
        
        # Validate required fields
        if not username:
            errors.append('El nombre de usuario es requerido.')
        elif len(username) < 3:
            errors.append('El nombre de usuario debe tener al menos 3 caracteres.')
            
        if not email:
            errors.append('El correo electrónico es requerido.')
            
        if not first_name:
            errors.append('El nombre es requerido.')
        elif len(first_name) < 3:
            errors.append('El nombre debe tener al menos 3 caracteres.')
            
        if not last_name:
            errors.append('Los apellidos son requeridos.')
        elif len(last_name) < 3:
            errors.append('Los apellidos deben tener al menos 3 caracteres.')
            
        if not password:
            errors.append('La contraseña es requerida.')
        if not password_confirm:
            errors.append('La confirmación de contraseña es requerida.')
        
        # Validate email format
        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append('El formato del correo electrónico no es válido.')
        
        # Validate password strength
        if password:
            if len(password) < 8:
                errors.append('La contraseña debe tener al menos 8 caracteres.')
            if not re.search(r'[A-Z]', password):
                errors.append('La contraseña debe contener al menos una letra mayúscula.')
            if not re.search(r'[0-9]', password):
                errors.append('La contraseña debe contener al menos un número.')
        
        # Validate password confirmation
        if password and password_confirm and password != password_confirm:
            errors.append('Las contraseñas no coinciden.')
        
        # Check username uniqueness
        if username and User.objects.filter(username=username).exists():
            errors.append('Este nombre de usuario ya está en uso.')
        
        # Check email uniqueness
        if email and User.objects.filter(email=email).exists():
            errors.append('Este correo electrónico ya está registrado.')
        
        if errors:
            # Return form with errors
            for error in errors:
                messages.error(request, error)
            return render(request, 'core/crear_cuenta.html', {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
            })
        
        # Create the user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            messages.success(request, '¡Cuenta creada exitosamente! Ya puedes iniciar sesión.')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error al crear la cuenta: {str(e)}')
            return render(request, 'core/crear_cuenta.html', {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
            })
    
    return render(request, 'core/crear_cuenta.html')