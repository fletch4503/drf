from django import forms
from .models import ewsitem


# Создаем класс формы для модели ewsitem
class ewsitemForm(forms.ModelForm):
    class Meta:
        model = ewsitem
        # Основные поля модели
        # email_title = models.CharField(max_length=250)  # Сюда вставляем заголовки писем с типом из exchangelib
        # sender = models.EmailField(max_length=254)  # адрес отправителя
        # time_receive = models.DateTimeField(auto_now_add=True)  # Время получения
        # done = models.BooleanField(default=False)  # Обработано
        # cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
        fields = ("email_title", "sender", "done", "cat")
        # Здесь будет переопределение полей
        email_title = forms.CharField(
            max_length=250,
            widget=forms.TextInput()
        )
        # fields = '__all__'
