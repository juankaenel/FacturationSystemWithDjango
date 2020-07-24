from django.urls import path
from core.erp.views.category.views import category_list
#nombre de las rutas de erp
app_name = 'erp'

urlpatterns=[
    path('category/list',category_list, name='category_list'),
]