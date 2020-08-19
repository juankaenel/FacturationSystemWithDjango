#Primer Método
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView #vista genérica login view, logout view
from django.shortcuts import redirect
import config.settings as setting
#Segundo Método
#from django.urls import reverse_lazy
#from django.views.generic import FormView
#from django.contrib.auth.forms import AuthenticationForm
#from django.contrib.auth import login
#from django.http import HttpResponseRedirect

from django.views.generic import RedirectView

# Vamos a mostrar dos métodos de login, son parecidos ambos puedes sobreescribir el método form_valid puesto que ambos
# implementan FormView la diferencia es que uno ya tiene el form y la validación del login.
# Yo utilizo el LoginView porque ya esta hecho no me preocupo por lo demás.

#Primer metodo de login  -> recomendable



class LoginFormView(LoginView):
    """
    Vista basada en clase LoginView
    """
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        #el usuario lo sacamos a través del request
        if request.user.is_authenticated: #si se encuentra logeado
            return redirect(setting.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar Sesión'
        return context

#Segundo método de login
# class LoginFormView2(FormView):
#     """
#     Vista genérica LoginFormView que hereda de  Form view
#     """
#     template_name = 'login.html'
#     form_class = AuthenticationForm
#     success_url = reverse_lazy(setting.LOGIN_REDIRECT_URL)
#
#
#     def dispatch(self, request, *args, **kwargs):
#         #el usuario lo sacamos a través del request
#         if request.user.is_authenticated: #si se encuentra logeado
#             return HttpResponseRedirect(self.success_url)
#         return super().dispatch(request, *args, **kwargs)
#
#     def form_valid(self, form):
#         login(self.request,form.get_user())
#         return HttpResponseRedirect(self.success_url)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Iniciar Sesión'
#         return context

#metodos de cierre de sesión

#el primer método llama a la vista genérica LogoutView directamente desde loginurls

#el segundo método de logout
#class LogoutRedirectView(RedirectView):
#    pattern_name = 'login' #página a donde se redirije una vez que cierre sesión
#
#    def dispatch(self, request, *args, **kwargs):
#        logout(request) #cierro sesión y voy al pattern_name
#        return super().dispatch(request, *args, **kwargs)

