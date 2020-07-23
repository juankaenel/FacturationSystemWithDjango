from config.wsgi import *
from core.erp.models import Type

#select * from
# query = Type.objects.all()
# print(query)

#Inserción
# t = Type() #hago una instancia de type
#
# t.name= 'Presidente'
# t.save()

# #Edición
# try:
#     t = Type.objects.get(pk=2) #llave duplicada
#     t.name = 'Vendedor'
#     t.save()
# except Exception as e:
#     print(e)

#Eliminación
# t = Type.objects.get(pk=1)
# t.delete()