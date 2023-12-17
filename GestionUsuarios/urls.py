from django.urls import path
from GestionUsuarios import views
from .views import Autenticacion, cerrar_sesion, signIn

urlpatterns = [

    path('autenticacion', Autenticacion.as_view(), name="Autenticacion"),

    path('cerrar_sesion', views.cerrar_sesion, name="cerrar_sesion"),

    path('signIn', views.signIn, name="signIn"),
]
