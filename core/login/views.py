from django.contrib.auth.views import LoginView #vista genérica login view
from django.shortcuts import redirect


class LoginFormView(LoginView):
    """
    Vista basada en clase LoginView
    """
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        #el usuario lo sacamos a través del request
        if request.user.is_authenticated: #si se encuentra logeado
            return redirect('erp:category_list')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar Sesión'
        return context
