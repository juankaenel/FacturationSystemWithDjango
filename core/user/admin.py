from django.contrib import admin

# Register your models here.
from core.user.models import User

admin.site.register(User) #con esto registro mi modelo en el panel de administración de django