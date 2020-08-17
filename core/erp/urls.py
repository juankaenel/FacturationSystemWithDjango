from django.urls import path
from core.erp.views.category.views import *
#nombre de las rutas de erp
app_name = 'erp'

urlpatterns=[
    path('category/list/',CategoryListView.as_view(), name='category_list'),
    path('category/add/',CategoryCreateView.as_view(), name='category_create'),
    path('category/edit/<int:pk>/',CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/',CategoryDeleteView.as_view(), name='category_delete'),
    path('category/form/<int:pk>/',CategoryFormView.as_view(), name='category_form'),
]