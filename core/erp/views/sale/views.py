import json
#django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, View

#core
from core.erp.forms import SaleForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Sale, Product, DetSale

#xhtml2pdf
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

class SaleListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Sale
    template_name = 'sale/list.html'
    permission_required = 'erp.view_sale'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Sale.objects.all():
                    data.append(i.toJson())
            elif action == 'search_details_prod':
                data = []
                for i in DetSale.objects.filter(sale_id=request.POST['id']): #filtro los detalles de la venta por id
                    data.append(i.toJson())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('erp:sale_create')
        context['list_url'] = reverse_lazy('erp:sale_list')
        context['entity'] = 'Ventas'
        return context

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
                    item = i.toJson()
                    item['value'] = i.name #el autocomplete tiene una variable value que necesita para poder presentarse en la busqueda cuando se va tecleando
                    data.append(item) #agrego el producto iterado al array data
            elif action == 'add':
                with transaction.atomic(): #meto toda la lógica dentro del transaction, esto me permite volver atrás en caso de que ocurra un error en el detalle o la factura, entonces no se guarda nada en caso de error.
                    #venta
                    vents = json.loads(request.POST['vents'])
                    sale = Sale()
                    sale.date_joined = vents['date_joined']
                    sale.client_id = vents['client']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()
                    #detalle de venta
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
        context['det'] = []
        return context

class SaleUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('index')
    permission_required = 'erp.change_sale'
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
                    item = i.toJson()
                    item['value'] = i.name #el autocomplete tiene una variable value que necesita para poder presentarse en la busqueda cuando se va tecleando
                    data.append(item) #agrego el producto iterado al array data
            elif action == 'edit':
                with transaction.atomic(): #meto toda la lógica dentro del transaction, esto me permite volver atrás en caso de que ocurra un error en el detalle o la factura, entonces no se guarda nada en caso de error.
                    #venta
                    vents = json.loads(request.POST['vents'])
                    sale = self.get_object()
                    sale.date_joined = vents['date_joined']
                    sale.client_id = vents['client']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()
                    sale.detsale_set.all().delete() #accedo a la relación detalle de venta, traigo todos los productos y los borro
                    #detalle de venta
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

    def get_details_product(self):
        data = []
        try:
            for i in DetSale.objects.filter(sale_id=self.get_object().id): #filtrame a los detalles por su id y iterame
                item = i.prod.toJson() #obtengo el producto en forma de diccionario
                item['cant'] = i.cant
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product()) #convierto a json el detalle del producto. Esto se renderizará en el create html, en el script linea 125
        return context

class SaleDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Sale
    template_name = 'sale/delete.html'
    success_url = reverse_lazy('erp:sale_list')
    permission_required = 'erp.delete_sale'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
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
        context['title'] = 'Eliminación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        return context

class SaleInvoicePdfView(View):
    def link_callback(self, uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path

    def get(self,request,*args,**kwargs):
        try:
            template = get_template('sale/invoice.html') #me devuelve el objeto en base a lo que le paso
            context = { #Estos serán renderizados en el invoice.html 
                'sale': Sale.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'Devkoders', 'ruc': '99999', 'address': 'Pres. Roque Saénz Peña, Chaco, Argentina'},
                #'icon': '{}{}'.format(settings.STATIC_URL, 'img/logo.png'),
                'icon': '{}'.format('img/logo.png'),
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
            # crear el pdf
            pisa_status = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            if pisa_status.err:
                return HttpResponse('Tenemos algunos errores <pre>' + html + '</pre>')
            return response #retorna el response, este contiene el pdf
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:sale_list'))
