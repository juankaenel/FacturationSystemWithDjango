from django.forms import *

from core.erp.models import Category


class CategoryForm(ModelForm):
    """
    Formulario de categoría
    """
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #for form in self.visible_fields():                     #con esto voy a evitar estar definiendo el tipo de clase del fomulario para cada dato del modelo, esta es una forma, la otra forma es con una libreria llamada widget_tweaks que solo se trabaja desde el front
        #    form.field.widget.attrs['class'] = 'form-control'                como voy a hacer uso de la libreria 'widget_tweaks' solo comento las lineas
        #    form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus']= True #poneme el foco en el name


    class Meta:
        model = Category
        fields = '__all__'  # columnas del formulario, todas. Tmb puedo presentar una exclusión exclude=['']
        #labels = { #con esto puedo modificar los labels del formulario en caso de no usar un verbose_name
        #    'name': 'Nombre'
        #}
        widgets = {  # con esto personalizo el tipo de entrada de dato de formulario, si es textarea, textinput
            'name': TextInput(
                attrs={
                    #'class': 'form-control',
                    'placeholder': 'Ingrese el nombre...',
                    #'autocomplete': 'off'
                }
            ),
            'desc': Textarea(
                attrs={
                    #'class': 'form-control',
                    'placeholder': 'Ingrese una descripción...',
                    #'autocomplete': 'off',
                    'rows':3,
                    'cols':3
                }
            )

        }
