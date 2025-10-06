from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('inicio')  # cambia esto al nombre de tu vista protegida
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'login.html')