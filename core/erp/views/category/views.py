#Django
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView   #Vistas genéricas
#erp
from core.erp.forms import CategoryForm
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

    @method_decorator(csrf_exempt) #decorador para habilitar el crsf
    #reescribimos el metodo dispatch
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        data = {}
        #print(request.POST)
        try:
            data = Category.objects.get(pk=request.POST['id']).toJson() #Si se comple llama al metodo toJson y me convierte los datos a diccinario
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    #sobreescribo el data a enviar debido a que se enviaba vacío
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] ='Listado de categorías'
        context['entity'] = 'Categorías' #esto viaja al body para que tome ese nombre el href
        context['create_url'] = reverse_lazy('erp:category_create')
        context['list_url'] = reverse_lazy('erp:category_list')
        return context

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm #le paso el formulario basado en clases
    template_name = 'category/create.html' #le paso el template
    success_url = reverse_lazy('erp:category_list') #una vez que se ejecute dicho formulario redireccioname a category list

    def post(self, request, *args, **kwargs):
        data = {}
        # print(request.POST)
        try:
            #data = Category.objects.get(
            #    pk=request.POST['id']).toJson()  # Si se comple llama al metodo toJson y me convierte los datos a diccinario
            action = request.POST['action']
            if action == 'add':
                form = self.get_form() #form = CategoryForm(request.POST)
                data = form.save() #llamo al metodo save de forms.py de category
            else:
                data['error'] = 'No ha especificado ninguna acción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] ='Crear categoría'
        context['entity'] = 'Categorías'
        context['list_url'] = reverse_lazy('erp:category_list')
        context['action'] = 'add' #action la usamos para verificar el tipo de acción se quiere realizar
        return context

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm  # le paso el formulario basado en clases
    template_name = 'category/create.html'  # le paso el template
    success_url = reverse_lazy('erp:category_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form() #form = CategoryForm(request.POST)
                data = form.save() #llamo al metodo save de forms.py de category
            else:
                data['error'] = 'No ha especificado ninguna acción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] ='Edición de una categoría'
        context['entity'] = 'Categorías'
        context['list_url'] = reverse_lazy('erp:category_list')
        context['action'] = 'edit' #action la usamos para verificar el tipo de acción se quiere realizar
        return context

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category/delete.html'  # le paso el template
    success_url = reverse_lazy('erp:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] ='Eliminación de una categoría'
        context['entity'] = 'Categorías'
        context['list_url'] = reverse_lazy('erp:category_list')
        context['action'] = 'edit' #action la usamos para verificar el tipo de acción se quiere realizar
        return context
