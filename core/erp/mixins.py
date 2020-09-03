from datetime import datetime

from django.shortcuts import redirect


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