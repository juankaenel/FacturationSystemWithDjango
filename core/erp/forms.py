from datetime import datetime

from django.forms import *

from core.erp.models import Category, Product, Client, Sale


class CategoryForm(ModelForm):
    """
    Formulario de categoría
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():                     #con esto voy a evitar estar definiendo el tipo de clase del fomulario para cada dato del modelo, esta es una forma, la otra forma es con una libreria llamada widget_tweaks que solo se trabaja desde el front
        #    form.field.widget.attrs['class'] = 'form-control'                como voy a hacer uso de la libreria 'widget_tweaks' solo comento las lineas
        #    form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True  # poneme el foco en el name

    class Meta:
        model = Category
        fields = '__all__'  # columnas del formulario, todas. Tmb puedo presentar una exclusión exclude=['']
        # labels = { #con esto puedo modificar los labels del formulario en caso de no usar un verbose_name
        #    'name': 'Nombre'
        # }
        widgets = {  # con esto personalizo el tipo de entrada de dato de formulario, si es textarea, textinput
            'name': TextInput(
                attrs={
                    # 'class': 'form-control',
                    'placeholder': 'Ingrese el nombre...',
                    # 'autocomplete': 'off'
                }
            ),
            'desc': Textarea(
                attrs={
                    # 'class': 'form-control',
                    'placeholder': 'Ingrese una descripción...',
                    # 'autocomplete': 'off',
                    'rows': 3,
                    'cols': 3
                }
            )

        }

        exclude = ['user_updated','user_creation'] #esto es para excluir que salgan estos campos en mi formulario

    # redefino el metodo save
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            print(e)
        return data

    # metodo que obtiene los errores del formulario
    def clean(self):
        cleaned = super().clean()
        if len(cleaned['name']) <= 3:  # si el campo nombre tiene menos de 50 caracteres salta el error
            self.add_error('name', 'Le faltan caracteres al campo')
            # raise forms.ValidationError('Validación xxx')
            # si uso esto en el html lo debo capturar con {{% form.non_field_errors  %}} y después en el script iterarlo
            # {% for error in form.non_field_errors %}
            #  errors += '{{error}}\n';
            # {%endfor%}
        # print(cleaned)
        return cleaned


class ProductForm(ModelForm):
    """
       Formulario de Producto
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True # poneme el foco en el name

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {  # con esto personalizo el tipo de entrada de dato de formulario, si es textarea, textinput
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'cat': Select(
                attrs={
                    'class': 'select2', #utilizo la libreria select2
                    'style': 'width: 100%'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ClientForm(ModelForm):
    """
    Formulario de Cliente
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True  # poneme el foco en el name

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {  # con esto personalizo el tipo de entrada de dato de formulario, si es textarea, textinput
            'names': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres...',
                }
            ),
            'surnames': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos...',
                }
            ),
            'dni': TextInput(
                attrs={
                    'placeholder': 'Ingrese su DNI...',
                }
            ),
            'date_brithday': DateInput(format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                }
            ),
            'address': TextInput(
                attrs={
                    'placeholder':'Ingrese su dirección',
                }
            ),
            'gender': Select()
        },
        exclude = ['user_updated','user_creation']


    # redefino el metodo save
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TestForm(Form):
    categories = ModelChoiceField(queryset=Category.objects.all(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    products = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    # search = CharField(widget=TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Ingrese una descripción'
    # }))

    search = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

class SaleForm(ModelForm):
    """
    Formulario de Sale/Venta
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():                     #con esto voy a evitar estar definiendo el tipo de clase del fomulario para cada dato del modelo, esta es una forma, la otra forma es con una libreria llamada widget_tweaks que solo se trabaja desde el front
           form.field.widget.attrs['class'] = 'form-control'                #como voy a hacer uso de la libreria 'widget_tweaks' solo comento las lineas
           form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['client'].widget.attrs['autofocus'] = True  # poneme el foco en el name
        self.fields['client'].widget.attrs['class'] =  'form-control select2'
        self.fields['client'].widget.attrs['style'] =  'width: 100%'

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {  # con esto personalizo el tipo de entrada de dato de formulario, si es textarea, textinput
            'client':Select(attrs={
                    'class': 'form-control',
                    'style': 'width:100%',
                }),
            'sale_date': DateInput(format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'value': datetime.now().strftime('%Y-%m-%d'), #valor por defecto
                }
                ),
        }

