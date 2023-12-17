from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

# Create your models here.

class Ingrediente(models.Model):

    nombre = models.CharField(max_length=50)

    lista_compra = models.ManyToManyField(
        User, 
        related_name='ingrediente_user',
        through="ListaCompra"
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'ingrediente'
        verbose_name_plural = 'ingredientes'

    def __str__(self):
        return self.nombre
    


class Receta(models.Model):

    autor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )

    usuario_loggeado = False
    
    titulo = models.CharField(
        max_length=100, 
        # null= False, 
        verbose_name='Título'
    )

    imagen = models.ImageField(
        upload_to='recetas/%d/%m/%Y',
        verbose_name='Imagen de la receta'
    )

    descripcion = models.TextField(
        verbose_name='Descripción de la receta',
        default=""
    )

    ingredientes_txt = models.TextField(
        verbose_name='Ingredientes',
        default=""
    )

    ingredientes = models.ManyToManyField(
        Ingrediente,    
        through="RecetaIngredientes"
    )

    likes = models.ManyToManyField(
        User, 
        related_name='receta_like'
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'receta'
        verbose_name_plural = 'recetas'
    
    def __str__(self):
        return self.titulo
    
    def numero_de_likes(self):
        return self.likes.count()
    
    def liked(self):
        return self.likes.filter(id=self.usuario_loggeado).exists()
    
    @classmethod
    def topRecetas(self, numRecetas=4):
        return self.objects.annotate(
            cnt=Count('likes')
        ).order_by('-cnt')[:numRecetas]
    
    @classmethod
    def ultimasRecetas(self):
        return self.objects.order_by('-updated')[:4]
    
class RecetaIngredientes(models.Model):
    receta = models.ForeignKey(
        Receta,
        null=False,
        related_name="cantidad",
        on_delete=models.CASCADE
    )

    ingrediente = models.ForeignKey(
        Ingrediente,
        null=False,
        related_name="cantidad",
        on_delete=models.CASCADE
    )

    cantidad = models.CharField(
        max_length=64   
    )
    
class ListaCompra(models.Model):
    user = models.ForeignKey(
        User,
        related_name="compra",
        on_delete=models.CASCADE
    )

    ingrediente = models.ForeignKey(
        Ingrediente,
        null=False,
        related_name="compra",
        on_delete=models.CASCADE
    )

    cantidad = models.CharField(
        max_length=64   
    )

   