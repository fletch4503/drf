from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from women.models import Women


# Телефонный номер для использования в модели ewsitem
class Contact(models.Model):
    person = Women()
    phone_number = models.CharField(
        max_length=20,  # Adjust based on your needs
        validators=[
            RegexValidator(
                regex=r'^\+?7?\d{10,10}$',  # Example regex for international phone numbers
                message="Phone number must be entered in the format: '+9999999999'. Up to 10 digits allowed."
            )
        ]
    )


# Каркас тестовой модели. Нужна модель всей таблицы Project
class ewsitem(models.Model):
    # Класс для работы с Exchange-сервером
    class Meta:
        ordering = ("-id",)  # со знаком '-' - обратная сортировка
        verbose_name = "EWS Item"
        verbose_name_plural = "EWS Items"

    # Основные поля модели
    email_title = models.CharField(max_length=250)  # Сюда вставляем заголовки писем с типом из exchangelib
    sender = models.EmailField(max_length=254)  # адрес отправителя
    time_receive = models.DateTimeField(auto_now_add=True)  # Время получения
    done = models.BooleanField(default=False)  # Обработано
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    archived = models.BooleanField(default=False)
    # phone_num = Contact.phone_number

    def get_absolute_url(self):
        # success_url = super().get_success_url()
        #     obj = self.object
        #     print(f'получили success_url: {success_url}, для объекта: {str(obj)}')
        #     additional_param = 'example_param'
        return reverse(
            "ews_list:detail",
            kwargs={"pk": self.pk},
        )
    # log.warning("Got some data. email_title: %s, sender: %s, done: %s", email_title, sender, done)

    def __str__(self):
        return self.email_title


class Category(models.Model):  # Категория полученных писем 1-ТСВ, 2-Поставщик, 3-ОП, 4 - Other
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name
