from django.db import models
from django.conf import settings

class BaseModel(models.Model):
    """
    Modelo base que será usado por algunos modelos para saber que usuarios fueron los que gestionaron ciertos registros
    user_creation y user_updated se deben definir el el método save de la clase que utilice éste modelo
    """
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='user_creation',null=True,blank=True)
    date_creation = models.DateTimeField(auto_now_add=True,null=True,blank=True) #me permite obtener por primera y unica vez el registro de la fecha
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_updated',null=True,blank=True)
    date_updated = models.DateTimeField(auto_now=True,null=True,blank=True)

    class Meta:
        abstract = True #este modelo no se va a crear en la tabla, sino que lo vamos a utilizar para implementarlo en otras entidades
