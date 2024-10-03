from django import forms
from .models import Women


# Создаем класс формы для модели ewsitem
class WomenForm(forms.ModelForm):
    class Meta:
        model = Women
        # Основные поля модели
        # title = models.CharField(max_length=255)
        # content = models.TextField(blank=True)
        # time_create = models.DateTimeField(auto_now_add=True)
        # time_update = models.DateTimeField(auto_now=True)
        # is_published = models.BooleanField(default=True)
        # cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
        fields = ("title", "content", "is_published", "cat")
        # Здесь будет переопределение полей
        widgets = {
            "content": forms.Textarea(attrs={"cols": 80, "rows": 3})
        }
        # fields = '__all__'
