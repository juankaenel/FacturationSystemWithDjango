#Django
from django.shortcuts import render
from django.views.generic import ListView

from core.erp.models import Category

#Vista basada en función
# def category_list(request):
#     data = {
#         'title' : 'Listado de categorías',
#         'categories' : Category.objects.all()
#     }
#     return render(request,'category/list.html',data)

#Vista basada en clase
class CategoryListView(ListView):
    model = Category
    template_name = 'category/list.html'

    #sobreescribo el data a enviar debido a que se enviaba vacío
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] ='Listado de categorías'
        return context
