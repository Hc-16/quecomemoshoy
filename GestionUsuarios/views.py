from django.shortcuts import render,HttpResponse,redirect
from django.template import Template
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages

# Create your views here.


class Autenticacion(View):
    
    def get(self, request):

        form = UserCreationForm()

        return render(request, "GestionUsuarios/signUp.html",{"form":form})

    def post(self, request):
        
        form = UserCreationForm(request.POST)

        if form.is_valid():

            usuario = form.save()

            login(request, usuario)

            return redirect('home')
        
        else:

            for mensaje in form.error_messages:
                messages.error(request, form.error_messages[mensaje])

            return render(request, "GestionUsuarios/signUp.html",{"form":form})


def cerrar_sesion(request):

    logout(request)

    return redirect('home')


def signIn(request):

    if request.method == "POST":

        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():

            nombre_usuario = form.cleaned_data.get("username")
            contrasenya = form.cleaned_data.get("password")

            usuario = authenticate(
                username= nombre_usuario,
                password = contrasenya
            )

            if usuario is not None:

                login(request, usuario)

                return redirect('home')
            
            else:
                messages.error(request, "usuario no válido")
        
        else: 
            messages.error(request, "infromación incorrecta")
            
    form = AuthenticationForm()

    return render(request, "GestionUsuarios/signIn.html",{"form":form})
