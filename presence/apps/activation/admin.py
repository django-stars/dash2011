from django.contrib import admin
from models import ActivationKey


class ActivationKeyAdmin(admin.ModelAdmin):
    list_display = ("__unicode__", "created")

admin.site.register(ActivationKey, ActivationKeyAdmin)
