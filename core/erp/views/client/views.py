from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.erp.models import Client


class ClientView(TemplateView):
    template_name = 'client/list.html'

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'datasearch':
                data = []
                for i in Client.objects.all():
                    data.append(
                        i.toJson())  # AGREGO a la lista data todos los objetos de la categoria en forma de diccionario
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=True)


    # sobreescribo el data a enviar debido a que se enviaba vacío
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de clientes'
        context['entity'] = 'Clientes'  # esto viaja al body para que tome ese nombre el href
        context['list_url'] = reverse_lazy('erp:client')
        return context