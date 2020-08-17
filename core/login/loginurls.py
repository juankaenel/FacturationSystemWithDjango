from django.urls import path
from core.erp.views.category.views import *
#nombre de las rutas de erp
from core.login.views import *

urlpatterns=[
    path('', LoginFormView.as_view(),name='login'), # /login
    path('logout/', LogoutView.as_view(next_page='login'),name='logout'), #login/logout
    #path('logout2/', LogoutRedirectView.as_view(),name='logout2'), #login/logout
    #path('', LoginFormView2.as_view()),

]