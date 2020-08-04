# Django
from django.db import models

# Local
from datetime import datetime

from django.forms import model_to_dict


class Category(models.Model):
    """
      Category Model
    """
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500,null=True,blank=True,verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJson(self): #convierte a json los datos
        #item = {'id': self.id,'name': self.name}
        item = model_to_dict(self,exclude=['']) #este metodo ya me transforma el modelo entero a diccionario asi no tenemos que estar definiendo como arriba
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
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cate = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True)
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'producto'
        ordering = ['id']

class Client(models.Model):
    """
    Client Model
    """
    names = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    last_names = models.CharField(max_length=150)
    dni = models.IntegerField()
    birth_date = models.DateTimeField()
    direction = models.CharField(max_length=50)
    sex = models.CharField(max_length=12)

    def __str__(self):
        return self.names

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
    sale_date = models.DateField(default=datetime.now)
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
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)     #FK
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)  #FK
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