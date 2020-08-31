# Django
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView  # Vistas genéricas
# erp
from core.erp.forms import CategoryForm
from core.erp.models import Category


# Vista basada en función
# def category_list(request):
#     data = {
#         'title' : 'Listado de categorías',
#         'categories' : Category.objects.all()
#     }
#     return render(request,'category/list.html',data)

# Vista basada en clase
class CategoryListView(ListView):
    model = Category
    template_name = 'category/list.html'

    @method_decorator(login_required) #debo definir el login_url en settings para la redireccion en caso q no esté logueado
    @method_decorator(csrf_exempt)  # decorador para deshabilitar el crsf
    # reescribimos el metodo dispatch
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # en caso de no usar muchos datos en tablas
    # def post(self,request,*args,**kwargs):
    #     data = {}
    #     #print(request.POST)
    #     try:
    #         data = Category.objects.get(pk=request.POST['id']).toJson() #Si se comple llama al metodo toJson y me convierte los datos a diccinario
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return JsonResponse(data)

    # en caso de usar muchos y que tarden mucho las peticiones vamos a hacer uso de ajax con datatables
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'datasearch':
                data = []
                for i in Category.objects.all():
                    data.append(i.toJson())  # AGREGO a la lista data todos los objetos de la categoria en forma de diccionario
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
           data['error'] = str(e)
        return JsonResponse(data, safe=False) #en este caso para serializar objeto que no están en formato diccionario hay que poner safe = False


# sobreescribo el data a enviar debido a que se enviaba vacío
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de categorías'
        context['entity'] = 'Categorías'  # esto viaja al body para que tome ese nombre el href
        context['create_url'] = reverse_lazy('erp:category_create')
        context['list_url'] = reverse_lazy('erp:category_list')
        return context

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm  # le paso el formulario basado en clases
    template_name = 'category/create.html'  # le paso el template
    success_url = reverse_lazy(
        'erp:category_list')  # una vez que se ejecute dicho formulario redireccioname a category list

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        #self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        # print(request.POST)
        try:
            # data = Category.objects.get(
            #    pk=request.POST['id']).toJson()  # Si se comple llama al metodo toJson y me convierte los datos a diccinario
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()  # form = CategoryForm(request.POST)
                data = form.save()  # llamo al metodo save de forms.py de category
            else:
                data['error'] = 'No ha especificado ninguna acción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear categoría'
        context['entity'] = 'Categorías'
        context['list_url'] = reverse_lazy('erp:category_list')
        context['action'] = 'add'  # action la usamos para verificar el tipo de acción se quiere realizar
        return context

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm  # le paso el formulario basado en clases
    template_name = 'category/create.html'  # le paso el template
    success_url = reverse_lazy('erp:category_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()  # form = CategoryForm(request.POST)
                data = form.save()  # llamo al metodo save de forms.py de category
            else:
                data['error'] = 'No ha especificado ninguna acción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una categoría'
        context['entity'] = 'Categorías'
        context['list_url'] = reverse_lazy('erp:category_list')
        context['action'] = 'edit'  # action la usamos para verificar el tipo de acción se quiere realizar
        return context

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category/delete.html'  # le paso el template
    success_url = reverse_lazy('erp:category_list')

    @method_decorator(login_required)
    # method_decorator(csrf_exempt) #con esto me evito enviarle parametros en ajax a través del data
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()  # la asignamos para que pueda hacer uso en el metodo post
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una categoría'
        context['entity'] = 'Categorías'
        context['list_url'] = reverse_lazy('erp:category_list')
        context['action'] = 'edit'  # action la usamos para verificar el tipo de acción se quiere realizar
        return context

class CategoryFormView(FormView):
    """
    Verifica que mi formulario sea válido y retornará hacia la url de éxito
    """
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('erp:category_list')

    # def form_invalid(self, form):
    #     print(form.is_valid()) #true o false si es valido
    #     print(form.errors)
    #     return super().form_invalid(form)
    #
    # def form_valid(self, form):
    #     print(form.is_valid())
    #     return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Form | Categoría'
        context['entity'] = 'Categorías'
        context['list_url'] = reverse_lazy('erp:category_list')
        context['action'] = 'add'  # action la usamos para verificar el tipo de acción se quiere realizar
        return context