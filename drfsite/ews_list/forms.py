from django import forms
from .models import ewsitem


# Создаем класс формы для модели ewsitem
class ewsitemCreateForm(forms.ModelForm):
    class Meta:
        model = ewsitem
        # Основные поля модели
        # email_title = models.CharField(max_length=250)  # Сюда вставляем заголовки писем с типом из exchangelib
        # sender = models.EmailField(max_length=254)  # адрес отправителя
        # time_receive = models.DateTimeField(auto_now_add=True)  # Время получения
        # done = models.BooleanField(default=False)  # Обработано
        # cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
        fields = ("email_title", "sender", "done", "cat")
        # Здесь будет переопределение полей из Exchangelib
        email_title = forms.CharField(
            max_length=250,
            widget=forms.TextInput()
        )
        help_texts = {
            "email_title": "Тема самого письма",
        }


class ewsitemUpdateForm(forms.ModelForm):
    class Meta(ewsitemCreateForm.Meta):
        fields = (
            "email_title",
            "sender",
            "done",
            "cat",
        )
