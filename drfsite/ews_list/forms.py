from django import forms
from .models import ewsitem


# Создаем класс формы для модели ewsitem
class ewsitemForm(forms.ModelForm):
    class Meta:
        model = ewsitem
        fields = '__all__'
