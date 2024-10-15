from django.contrib import admin
from ews_list.models import ewsitem


# admin.site.register(ewsitem)
# Register your models here.

@admin.register(ewsitem)
class ewsitemAdmin(admin.ModelAdmin):
    list_display = "id", "email_title", "sender", "visible", "done", "time_receive", "cat"
    list_display_links = "id", "email_title", "time_receive"

    def visible(self, obj: ewsitem) -> bool:
        return not obj.archived

    visible.boolean = True
