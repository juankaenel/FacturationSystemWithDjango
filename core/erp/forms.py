from django.forms import ModelForm

from core.erp.models import Category


class CategoryForm(ModelForm):
    """
    Formulario de categoría
    """
    class Meta:
        model = Category
        fields = '__all__'                                  #columnas del formulario, todas. Tmb puedo presentar una exclusión exclude=['']
