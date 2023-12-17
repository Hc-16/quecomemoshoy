from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template
from .models import Receta, Ingrediente, ListaCompra
from django.contrib.auth.models import User
from GestionRecetas.forms import FormularioCrearReceta
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
import re

def home(request):
    top_recetas = Receta.topRecetas()
    ult_recetas = Receta.ultimasRecetas()

    usuario_id = None
    if request.user:
        usuario_id = request.user.id

    for receta in top_recetas:
        receta.usuario_loggeado = usuario_id

    for receta in ult_recetas:
        receta.usuario_loggeado = usuario_id

    return render(
        request, 
        "GestionRecetas/index.html",
        {"top_recetas": top_recetas,
         "ult_recetas": ult_recetas
        }
    )

def todasRecetas(request):

    recetas = Receta.objects.all()

    usuario_id = None
    if request.user:
        usuario_id = request.user.id

    for receta in recetas:
        receta.usuario_loggeado = usuario_id
    
    return render(
        request, 
        "GestionRecetas/recetas.html",
        {"recetas": recetas}
    )

def misRecetas(request):
    usuario = request.user
    usuario_id = usuario.id
    recetas = Receta.objects.filter(autor = usuario_id)

    for receta in recetas:
        receta.usuario_loggeado = usuario_id

    return render(
        request, 
        "GestionRecetas/mis_recetas.html", 
        {'recetas': recetas}
    )   

@login_required
def creacionRecetas(request):
    miFormulario = FormularioCrearReceta()          
    # form = FormularioCrearReceta()
    return render(
        request,
        "GestionRecetas/creacion_recetas.html",
        { "form": miFormulario} 
    )

def procesar_ingredientes(lista):
    # "4 #tomates; 8 #peras; 6 #manzanas"
    ingredientes_add = []
    lineas = lista.split("\n")
    for linea in lineas:
        cantidad_nombre = linea.split("#")
        if len(cantidad_nombre) == 2:
            nombre_ing = re.sub(r'[^A-Za-z0-9 áéíóúÁÉÍÓÚñÑ]+', '', cantidad_nombre[1])
            nombre_ing = cantidad_nombre[1].strip().capitalize()
            if len(nombre_ing) >= 3:
                ingr, created = Ingrediente.objects.get_or_create(
                    nombre=nombre_ing
                )
                ingredientes_add.append([cantidad_nombre[0] or '*', ingr])

    return ingredientes_add

def crear(request):
    if request.method == "POST":
        ingredientes_add = procesar_ingredientes(request.POST["ingredientes_txt"])
        miFormulario = FormularioCrearReceta(request.POST, request.FILES) 

        listado_ingredientes_txt = []
        for ing in ingredientes_add:
            listado_ingredientes_txt.append(f"{ing[0]} #{ing[1]}")

        miFormulario.instance.autor = request.user
        if miFormulario.is_valid(): 
            miFormulario.instance.ingredientes_txt = ", ".join(listado_ingredientes_txt)
            receta = miFormulario.save()

            for i in ingredientes_add:
                receta.ingredientes.add(
                    i[1].id,
                    through_defaults={'cantidad': i[0]}
                )
            receta.save()
            messages.success(request, "Receta creada correctamente.")
            return redirect('detalles_receta', id=receta.id)
     
          
        else:
            return render(
                request,
                "GestionRecetas/creacion_recetas.html",
                { "form": miFormulario} 
            )
      
        return HttpResponseRedirect("/")
        
    else:
        return creacionRecetas(request)

def buscar(request):
   
    recipe = request.GET["rct"]
    recetas = []
    
    if recipe:
        ingrediente = Ingrediente.objects.filter(
            nombre__icontains=recipe
        )
        usuario = User.objects.filter(
            username__icontains=recipe
        )     
        
        recetas = (Receta.objects.filter(
            titulo__istartswith=recipe
        ) |  Receta.objects.filter(
            ingredientes__in=ingrediente
        ) | Receta.objects.filter(
            autor__in=usuario
        )).distinct()

    return render(
        request, 
        "GestionRecetas/result_busqueda.html", 
        {"recetas":recetas, "query":recipe}
    )



def editar(request, id):
    receta = Receta.objects.get(pk=id)
    edic_form = FormularioCrearReceta(instance=receta)
    
    if request.user.id != receta.autor.id:
        return redirect('home')

    return render(
         request, 
        "GestionRecetas/edicion_recetas.html", 
        {"form":edic_form, "receta": receta}
    )


def edicion(request, id):
    receta = Receta.objects.get(pk=id)

    if not receta or request.user.id != receta.autor.id:
        return redirect('home')

    if request.method == 'POST':
            edic_form = FormularioCrearReceta(
                request.POST, 
                request.FILES,
                instance=receta
            )

            if edic_form.is_valid():
                
                edic_form.save()
                messages.success(
                    request,
                    "La receta ha sido actualizada correctamente."
                )

            return redirect('detalles_receta', id=receta.id)
    else:
        edic_form = FormularioCrearReceta(instance=receta)
        return render(
            request, "GestionRecetas/edicion_recetas.html", {'form': edic_form}
        ) 


def eliminar(request, id):
    receta = Receta.objects.get(pk=id)
    receta.delete()

    messages.warning(
        request,
        "Se ha eliminado la receta correctamente."
    )

    return redirect('misRecetas')


def darLike(request, id):
    receta = get_object_or_404(
        Receta, 
        id=id
    )
    if receta.likes.filter(id=request.user.id).exists():
        receta.likes.remove(request.user)
    else:
        receta.likes.add(request.user)

    return redirect(request.META['HTTP_REFERER'])


def detalles_receta(request, id):
    receta = get_object_or_404(
        Receta, 
        id=id
    )
          
    if request.user:
        receta.usuario_loggeado = request.user.id


    editable = request.user.id == receta.autor.id
    top_recetas = Receta.topRecetas()

    for r in top_recetas:
        r.usuario_loggeado = request.user.id

    return render(
        request, "GestionRecetas/detalles_receta.html",
        {
            "receta": receta,
            "top_recetas": top_recetas,
            "editable": editable
        }
    )


def listaCompra(request):
    return render(
        request, "GestionRecetas/lista_de_compra.html"
    )
 
def addListaCompra(request, id):
    receta = get_object_or_404(
        Receta, 
        id=id
    )

    for c in receta.cantidad.all():
        ListaCompra.objects.create(
            user=request.user,
            ingrediente=c.ingrediente,
            cantidad=c.cantidad
        )

    return redirect('listaCompra')

@login_required
def vaciarListaCompra(request):
    request.user.compra.all().delete()
    
    messages.warning(
        request,
        "Se ha vaciado la lista de la compra."
    )

    return redirect(request.META['HTTP_REFERER'])
    

   