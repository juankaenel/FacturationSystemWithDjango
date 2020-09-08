from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from core.erp.forms import ProductForm
from core.erp.models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'product/list.html'

    @method_decorator(
        login_required)  # debo definir el login_url en settings para la redireccion en caso q no esté logueado
    @method_decorator(csrf_exempt)  # decorador para deshabilitar el crsf
    # reescribimos el metodo dispatch
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # sobreescribo el data a enviar debido a que se enviaba vacío
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['entity'] = 'Productos'  # esto viaja al body para que tome ese nombre el href
        context['create_url'] = reverse_lazy('erp:product_create')
        context['list_url'] = reverse_lazy('erp:product_list')
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm  # le paso el formulario basado en clases
    template_name = 'product/create.html'  # le paso el template
    success_url = reverse_lazy(
        'erp:product_list')  # una vez que se ejecute dicho formulario redireccioname a category list

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            #print(request.POST)
            #print(request.FILES)
                action = request.POST['action']
                if action == 'add':
                    form = self.get_form()
                    data = form.save()
                else:
                    data['error'] = 'No ha especificado ninguna acción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear producto'
        context['entity'] = 'Productos'
        context['list_url'] = reverse_lazy('erp:product_list')
        context['action'] = 'add'  # action la usamos para verificar el tipo de acción se quiere realizar
        return context


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm  # le paso el formulario basado en clases
    template_name = 'product/create.html'  # le paso el template
    success_url = reverse_lazy('erp:product_list')

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
        context['title'] = 'Edición de un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = reverse_lazy('erp:product_list')
        context['action'] = 'edit'  # action la usamos para verificar el tipo de acción se quiere realizar
        return context


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product/delete.html'  # le paso el template
    success_url = reverse_lazy('erp:product_list')

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
        context['title'] = 'Eliminación de un producto'
        context['entity'] = 'Productos'
        context['list_url'] = reverse_lazy('erp:product_list')
        context['action'] = 'edit'  # action la usamos para verificar el tipo de acción se quiere realizar
        return context
