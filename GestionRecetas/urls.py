from django.urls import path
from GestionRecetas import views


urlpatterns = [
    path('', views.home, name="home"),

    path('misRecetas', views.misRecetas, name="misRecetas"),

    path('creacionRecetas/', views.creacionRecetas, name="creacionRecetas"),

    path('crear/', views.crear, name="crear"),

    # path('busquedaRecetas/', views.busquedaRecetas, name="busquedaRecetas"),

    path('buscar/', views.buscar, name="buscar"),

    path('editar/<int:id>/', views.editar, name="editar"),

    path('edicion/<int:id>/', views.edicion, name="edicion"),

    path('eliminar/<int:id>/', views.eliminar, name="eliminar"),

    path('receta_like/<int:id>/', views.darLike, name="receta_like"),

    path('detalles_receta/<int:id>/', views.detalles_receta, name="detalles_receta"),

    path('todasRecetas/', views.todasRecetas, name="todasRecetas"),

    path('addListaCompra/<int:id>/', views.addListaCompra, name="addListaCompra"),

    path('listaCompra/', views.listaCompra, name="listaCompra"),

    path('vaciarListaCompra/', views.vaciarListaCompra, name="vaciarListaCompra"),

]