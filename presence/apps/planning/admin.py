from django.contrib import admin

from models import DayPlan


class DayPlanAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'date', 'work_status')

admin.site.register(DayPlan, DayPlanAdmin)
