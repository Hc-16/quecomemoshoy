from django import forms
from .models import Receta

class FormularioCrearReceta(forms.ModelForm):
    class Meta:
        model = Receta
        fields = '__all__'
        exclude = ['autor', 'likes', 'ingredientes']
        help_texts = {
            'ingredientes_txt': 'Una linea por ingrediente con formato: cantidad #nombre de ingrediente.',
        }
        widgets = {
            'ingredientes_txt': forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': 'Ejemplo:\n2 #huevos\n1 #tomate\n....'
                }
            ),
        }
