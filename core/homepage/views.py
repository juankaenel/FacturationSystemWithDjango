from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Se encarga de renderizar/presentar una plantilla que le mandamos por parametro en el template name"""
    template_name = 'index.html'