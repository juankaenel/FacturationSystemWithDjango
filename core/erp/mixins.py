from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy


class IsSuperUserMixin(object):
    """
    Método mixin que me permite controla que el usuario que esté ingresando a una vista sea superusuario, sino se lo redirije a otra vista.
    También le mando un contexto, para la fecha actual.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('index')

    def get_context_data(self, **kwargs):
        """
        Para enviarle la fecha actual al list del template principal
        """
        context = super().get_context_data(**kwargs)
        context['date_now'] = datetime.now()
        return context

class ValidatePermissionRequiredMixin(object):
    """
    Método mixin para controlar los permisos que tiene un usuario y la url a donde se va a redirigir en caso q no tenga dichos permisos
    """
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        if isinstance(self.permission_required,str): #si es un string, convierto en una tupla de un solo valor
            perms = (self.permission_required,)
        else:
            perms = self.permission_required #caso contrario mandamos toda la tupla
        return perms

    #validamos la url
    def get_url_redirect(self):
        if self.url_redirect is None: #si la url está vacia, retornar al login
            return reverse_lazy('login')
        #else
        return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perms(self.get_perms()): #con esto controlamos el tipo de permiso
            return super().dispatch(request, *args, **kwargs)
        #else
        messages.error(request,'No tiene permiso para ingresar') # itero los errores en el body.html
        return redirect(self.get_url_redirect())
