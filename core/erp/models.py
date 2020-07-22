from django.db import models
from datetime import datetime

class Type(models.Model):
    """
    Type Model, related to one to many with employee
    """
    name = models.CharField(max_length=150, verbose_name='Nombre')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo' #Nombre que lleva cuando registre mi aplicación en el modulo de administración de django
        verbose_name_plural = 'Tipos'
        db_table = 'tipo' #nombre de la tabla
        ordering = ['id'] #ordena por id de forma ascendente, si queremos que sea descendente [-id]


class Category(models.Model):
    """
      Category Model, related to many to many with employee
    """
    name = models.CharField(max_length=150, verbose_name='Nombre')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoria'  # Nombre que lleva cuando registre mi aplicación en el modulo de administración de django
        verbose_name_plural = 'Categorias'
        db_table = 'categoria'  # nombre de la tabla
        ordering = ['id']  # ordena por id de forma ascendente, si queremos que sea descendente [-id]


class Employee(models.Model):
    """
    Employee Model
    """
    category = models.ManyToManyField(Category)
    type = models.ForeignKey(Type,on_delete=models.CASCADE)  #tabla de pertenencia le pertence el fk, un empleado tiene un tipo, y un tipo puede tener muchos empleados
    names = models.CharField(max_length=150,verbose_name='Nombres')
    dni = models.CharField(max_length=10,unique=True,verbose_name='Dni')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    date_creation = models.DateField(auto_now=True) #solo se actualiza cuando se crea a la fecha actual
    date_updated = models.DateTimeField(auto_now_add=True) #se actualiza cada vez que se cambia algo en la tabla gracias al _add
    age = models.PositiveIntegerField(default=0)
    salary = models.DecimalField(default=0.00, max_digits=9, decimal_places=2) #hasta 9 y la coma hasta 2
    state = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', null=True, blank=True) # la imagen se guarda en la carpeta avatar con el orden de año mes y dia
    cvitae = models.FileField(upload_to='cvitae/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.names

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        db_table = 'empleado'
        ordering = ['id']


