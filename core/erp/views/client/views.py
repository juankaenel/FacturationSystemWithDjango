from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.erp.forms import ClientForm
from core.erp.mixins import IsSuperUserMixin
from core.erp.models import Client


class ClientView(LoginRequiredMixin,IsSuperUserMixin,TemplateView):
    template_name = 'client/list.html'

    @method_decorator(csrf_exempt)
    #@method_decorator(login_required) -> voy a usar el mixin para que controle el login
    def dispatch(self, request, *args, **kwargs): #al heredar el IsSuperMixin no tengo que controlar si es superusuario o no aquí en el dispatch sino que lo heredamos ya desde el mixins..
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            #acción para listar en los atributos del cliente datatable
            if action == 'datasearch':
                data = []
                for i in Client.objects.all():
                    data.append(i.toJson())
            #acción agregar
            elif action == 'add':
                cli = Client()
                cli.names = request.POST['names']
                cli.surnames = request.POST['surnames']
                cli.dni = request.POST['dni']
                cli.date_birthday = request.POST['date_birthday']
                cli.address = request.POST['address']
                cli.gender = request.POST['gender']
                cli.save()
            #acción editar
            elif action == 'edit':
                cli = Client.objects.get(pk=request.POST['id'])
                cli.names = request.POST['names']
                cli.surnames = request.POST['surnames']
                cli.dni = request.POST['dni']
                cli.date_birthday = request.POST['date_birthday']
                cli.address = request.POST['address']
                cli.gender = request.POST['gender']
                cli.save()
            #acción eliminar
            elif action == 'delete':
                cli = Client.objects.get(pk=request.POST['id'])
                cli.delete()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Clientes'
        context['list_url'] = reverse_lazy('erp:client')
        context['entity'] = 'Clientes'
        context['form'] = ClientForm()
        return context