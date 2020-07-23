from config.wsgi import *
from core.erp.models import Type, Employee

# # Listar (select * from)
# query = Type.objects.all()
# print(query)

# # Inserción
# t = Type() #hago una instancia de type
#
# t.name= 'Presidente'
# t.save()

# # Edición
# try:
#     t = Type.objects.get(pk=2) #llave duplicada
#     t.name = 'Vendedor'
#     t.save()
# except Exception as e:
#     print(e)

# # Eliminación
# t = Type.objects.get(pk=1)
# t.delete()

#Consultas de nombres
Type.objects.filter(name__icontains='pre') #icontains incluye mayusculas y minusculas entonces puede traer el Presidente

Type.objects.filter(name__startswith='p') #empieza con p

Type.objects.filter(name__endswith='p') #termina con p


Type.objects.filter(name__in=['Presidente','Gerente']) #traeme esos tipos
Type.objects.filter(name__in=['Presidente','Gerente']).count() #traeme esos tipos y contame cuantos son
Type.objects.filter(name__contains='Presidente').query  #con query obtengo el código de la consulta en sql

Type.objects.filter(name__endswith='p').exclude(pk=5) #traeme estos que terminan en p exceptuando al de id 5

for i in Type.objects.filter(name__icontains='pre')[1]: #traeme un solo registro
    print(i.name)

for i in Type.objects.filter(name__icontains='pre')[:2]:  #los primeros 2. Y así ir probando con el rebanado
    print(i.name)


#trabajando con tablas relacionadas

Employee.objects.filter(type_id=1) #el tipo de empleado con type id 1







