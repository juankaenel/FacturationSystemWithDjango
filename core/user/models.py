from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import MEDIA_URL, STATIC_URL


class User(AbstractUser):
    """
    Función para modificar el modelo usuario por defecto en django
    """
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True,verbose_name='Imágen') #agrego el campo nuevo al modelo

    def get_image(self):
        """
        Función para determinar la ruta absoluta de la imágen
        """
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL,'img/empty.png') # si no llega a tener una imagen me da una imagen por defecto


