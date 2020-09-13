# Django
from crum import get_current_user
from django.db import models

# Local
from datetime import datetime

from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import gender_choices
from core.models import BaseModel


class Category(BaseModel):
    """
      Category Model, hereda de BaseModel para saber que usuario gestionó ciertos registros y en qué momento, para eso redefine su método save donde hace uso de una librería django-crum
    """
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # acá le digo que va a pasar cuando haga un guardado -> https://pythonhosted.org/django-crum/
        user = get_current_user()
        if user is not None: #si el usr no está vacío
            if not self.pk: # si no tiene su clave primaria, significa q estoy haciendo una creación
                self.user_creation = user #usa la propiedad del modelo Base Model en caso que se cree una nueva categoria
            else:
                self.user_updated = user #si existe el la relación la actualizo -> en caso que se modifique una categoría
        #con esto obtengo el usuario que se está creando o actualizando
        super(Category, self).save()

    def toJson(self):  # convierte a json los datos
        # item = {'id': self.id,'name': self.name}
        item = model_to_dict(self, exclude=[
            ''])  # este metodo ya me transforma el modelo entero a diccionario asi no tenemos que estar definiendo como arriba
        return item

    class Meta:
        verbose_name = 'Categoria'  # Nombre que lleva cuando registre mi aplicación en el modulo de administración de django
        verbose_name_plural = 'Categorias'
        db_table = 'categoria'  # nombre de la tabla
        ordering = ['id']  # ordena por id de forma ascendente, si queremos que sea descendente [-id]


class Product(models.Model):
    """
    Product Model
    """
    name = models.CharField(max_length=150, verbose_name='Nombre',
                            unique=True)  # el verbose name es como se verá en el formulario
    cate = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imágen')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['cat'] = self.cate.toJson()
        item['image'] = self.get_image()
        item['pvp'] = format(self.pvp, '.2f')
        return item

    def get_image(self):
        if self.image:
            return (f'{MEDIA_URL}{self.image}')
        else:
            return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'producto'
        ordering = ['id']


class Client(models.Model):
    """
    Client Model
    """
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150,verbose_name='Apellidos')
    dni = models.IntegerField(unique=True, verbose_name='DNI')
    date_birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=14,choices=gender_choices,default='male',verbose_name='Sexo')

    def __str__(self):
        return self.names

    def toJson(self):  # convierte a json los datos
        item = model_to_dict(self) #paso el modelo a diccionario
        item['gender'] = {'id':self.gender, 'name': self.get_gender_display()}
        #item['date_birthday'] = self.date_birthday.strftime('%d/%m/%Y')
        item['date_birthday'] = self.date_birthday.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'cliente'
        ordering = ['id']


class Sale(models.Model):
    """
        Sale Model
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)  # FK, tabla de pertenencia
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.client

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventass'
        db_table = 'venta'
        ordering = ['id']


class DetSale(models.Model):
    """
        DetSale Model
    """
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)  # FK
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)  # FK
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.sale

    class Meta:
        verbose_name = 'Detalle Venta'
        verbose_name_plural = 'Detalles de ventas'
        db_table = 'detalle_venta'
        ordering = ['id']
