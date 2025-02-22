from django.db import models
from django.urls import reverse


class Women(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)

    class Meta:
        ordering = ("id",)  # со знаком '-' - обратная сортировка
        verbose_name = "Women Item"
        verbose_name_plural = "Women Items"

    def get_absolute_url(self):
        # success_url = super().get_success_url()
        #     obj = self.object
        #     print(f'получили success_url: {success_url}, для объекта: {str(obj)}')
        #     additional_param = 'example_param'
        return reverse(
            "women:detail",
            kwargs={"pk": self.pk},
        )

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name
