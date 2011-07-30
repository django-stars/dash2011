from django.contrib import admin

from models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'updated')

admin.site.register(Profile, ProfileAdmin)
