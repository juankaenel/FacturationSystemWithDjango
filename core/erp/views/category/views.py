# Django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView  # Vistas genéricas
# erp
from core.erp.forms import CategoryForm
from core.erp.mixins import IsSuperUserMixin, ValidatePermissionRequiredMixin
from core.erp.models import Category


# Vista basada en función
# def category_list(request):
#     data = {
#         'title' : 'Listado de categorías',
#         'categories' : Category.objects.all()
#     }
#     return render(request,'category/list.html',data)

# Vista basada en clase

class CategoryListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Category
    template_name = 'category/list.html'
    #permisos requeridos son los que te obligan a tener ese permiso para poder ingresar a la vista, si un usr no lo tiene no lo dejará entrar
    #permission_required = ('erp.change_category','erp.delete_category') # estos permisos lo definí desde el panel de administración, en la parte usuarios. Si no tiene habilitado este permiso y no es un super usuario le tirará error Forbbiden. También se crea una tabla nueva en la bd llamada user_permissions que es donde se guardan las relaciones de los permisos
    #puedo hacer uso de PermissionRequiredMixin -> que ya está definido en django pero en este caso creamos una nueva desde el mixins.py llamada validatepermissionrequiredmixin
    #permission_required = ('erp.change_category','erp.delete_category') #estos dos permisos si los tengo
    permission_required = ('erp.view_category','erp.delete_category') #el view no lo tengo por lo tanto me redirijirá al dashboard
    #permission_required = ('erp.delete_category') #el view no lo tengo por lo tanto me redirijirá al dashboard



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
        context['title'] = 'Listado de Categorías'
        context['entity'] = 'Categorías'  # esto viaja al body para que tome ese nombre el href
        context['create_url'] = reverse_lazy('erp:category_create')
        context['list_url'] = reverse_lazy('erp:category_list')
        return context

class CategoryCreateView(ValidatePermissionRequiredMixin,CreateView):
    #control de acceso
    permission_required = 'erp.view_category'
    url_redirect = reverse_lazy('erp:category_list')
    #fin del control
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