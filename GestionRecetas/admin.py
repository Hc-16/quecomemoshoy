from django.contrib import admin
from .models import Receta, Ingrediente
# Register your models here.

class IngredienteAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

class RecetaAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')


admin.site.register(Receta, RecetaAdmin)
admin.site.register(Ingrediente, IngredienteAdmin)
