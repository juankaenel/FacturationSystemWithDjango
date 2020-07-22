from django.db import models
from datetime import datetime

class Employee(models.Model):
    """
    Employee Model
    """
    names = models.CharField(max_length=150,verbose_name='Nombres')
    dni = models.CharField(max_length=10,unique=True,verbose_name='Dni')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    created_at = models.DateField(auto_now=True) #solo se actualiza cuando se crea a la fecha actual
    date_updated = models.DateTimeField(auto_now_add=True) #se actualiza cada vez que se cambia algo en la tabla gracias al _add
    age = models.PositiveIntegerField(default=0)
    salary = models.DecimalField(default=0.00, max_digits=9, decimal_places=2) #hasta 9 y la coma hasta 2
    state = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', null=True, blank=True) # la imagen se guarda en la carpeta avatar con el orden de año mes y dia
    cvitae = models.FileField(upload_to='cvitae/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.names

    class Meta:
        verbose_name = 'Empleado' #cuando registre mi aplicación en el modulo de administración de django
        verbose_name_plural = 'Empleados'
        db_table = 'empleado' #nombre de la tabla
        ordering = ['id'] #ordena por id de forma ascendente, si queremos que sea descendente [-id]


