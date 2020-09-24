import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView

from core.erp.forms import SaleForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Sale, Product, DetSale


class SaleCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('index')
    permission_required = 'erp.add_sale'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data=[]
                prods = Product.objects.filter(name__icontains=request.POST['term'])[0:10] #guardo los productos que vienen por el form.js en la variable term pero solo diez productos
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.name #el autocomplete tiene una variable value que necesita para poder presentarse en la busqueda cuando se va tecleando
                    data.append(item) #agrego el producto iterado al array data
            elif action == 'add':
                vents = json.loads(request.POST['vents'])
                sale = Sale()
                sale.date_joined = vents['date_joined']
                sale.client_id = vents['client']
                sale.subtotal = float(vents['subtotal'])
                sale.iva = float(vents['iva'])
                sale.total = float(vents['total'])
                sale.save()

                for i in vents['products']:
                    detalle = DetSale()
                    detalle.sale_id = sale.id
                    detalle.prod_id = i['id']
                    detalle.cant = int(i['cant'])
                    detalle.price = float(i['pvp'])
                    detalle.subtotal = float(i['subtotal'])
                    detalle.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False) #para que se pueda serializar indico que el safe=false

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


